from typing import List

from fastapi import APIRouter, HTTPException, Request, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Project
from resume_assist.io.db.engine import neo4j_client
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent
from resume_assist.agent_hub.keyword_extraction_agent import KeywordExtractionAgent
from resume_assist.agent_hub.retrieval_agent import RetrievalAgent
from resume_assist.agent_hub.summary_agent import SummaryAgent
from resume_assist.agent_hub.reviewer_agent import ReviewerAgent
from resume_assist.utilities.formatting_utils import (
    build_full_job_description,
    build_reference_chunks_str,
    build_previous_attempt_str,
    build_highlight_str,
)


project_router = APIRouter(prefix="/api/project", tags=["Resume: Project Experience"])


@project_router.post("/save")
def save_project(request: List[Project]):
    try:
        for project in request:
            query = """
            MERGE (pr:Project {id: $project_id})
            SET
                pr.project_name = $project_name,
                pr.start_date = $start_date,
                pr.end_date = $end_date,
                pr.url = $url,
                pr.current = $current,
                pr.highlights = $highlights
            RETURN pr
            """
            parameters = {"project_id": str(project.project_id), **project.model_dump()}
            result = neo4j_client.query(query, parameters)
            if not result:
                raise HTTPException(500, "Failed to save personal information")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@project_router.get("/all", response_model=List[Project])
def get_project():
    try:
        query = """
        MATCH (pr:Project)
        RETURN pr
        """
        parameters = {}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Personal Information not found")

        projects = [Project(**record["pr"]) for record in result]
        return projects
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@project_router.post("/assist", response_model=List[str])
async def assist_project(request: Request):
    try:
        info_vars = await request.json()

        resume_info = info_vars["resume"]
        job_info = info_vars["job_details"]
        project_info = info_vars["project"]
        info_vars.update(**resume_info)
        info_vars.update(**job_info)
        info_vars.update(**project_info)

        summary_agent = SummaryAgent("project")
        keyword_agent = KeywordExtractionAgent("project")
        retrieval_agent = RetrievalAgent("project", use_prompt=False)
        enhancer_agent = EnhancerAgent("project")
        reviewer_agent = ReviewerAgent("project")

        job_description = build_full_job_description(
            info_vars["company"], info_vars["position"], info_vars["description"]
        )
        job_summary = summary_agent.step(
            {
                "company": info_vars["company"],
                "role": info_vars["position"],
                "job_description": info_vars["description"],
            }
        )

        enhancement_info: dict = {}
        enhancement_info["keywords"] = "; ".join(
            keyword_agent.extract_keywords(job_description)
        )
        enhancement_info["reference_chunks"] = build_reference_chunks_str(
            retrieval_agent.retrieve(
                indexer_txt=job_summary, node_type="Project", refined_filter=False
            ),
            chunk_parser=build_highlight_str,
        )
        enhancement_info["previous_attempt"] = ""
        enhancement_info["highlights"] = info_vars["highlights"]

        num_retries = 0
        while True:
            original_highlights = info_vars["highlights"]

            ai_assisted_highlights = enhancer_agent.step(enhancement_info.copy())
            grade, remark = reviewer_agent.review(
                original_highlights, ai_assisted_highlights, job_description
            )
            enhancement_info["last_enhanced_version"] = str(ai_assisted_highlights)
            enhancement_info["previous_attempt"] = build_previous_attempt_str(
                ai_assisted_highlights, remark
            )
            if grade >= 8:
                break
            if num_retries >= 3:
                print(
                    "Warning: The optimized version fails to pass AI reviewer, use at your own discretion."
                )
                break
            num_retries += 1
        return ai_assisted_highlights
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
