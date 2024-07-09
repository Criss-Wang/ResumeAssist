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


project_router = APIRouter(prefix="/project", tags=["Resume: Project Experience"])


@project_router.post("/{id}/save")
def save_project(id: UUID, request: Project):
    try:
        query = """
        MERGE (pr:Project {id: $id})
        SET
            pr.project_name = $project_name,
            pr.start_date = $start_date,
            pr.end_date = $end_date,
            pr.highlights = $highlights
        RETURN pr
        """
        parameters = {"id": str(id), **request.model_dump()}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(500, "Failed to save personal information")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@project_router.get("/{id}", response_model=Project)
def get_project(id: UUID):
    try:
        query = """
        MATCH (pr:Project {id: $id})
        RETURN pr
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Personal Information not found")
        project = result[0]["pr"]
        return Project(**project)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@project_router.post("/assist")
async def assist_project(request: Request):
    try:
        info_vars = await request.json()

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
        info_vars["keywords"] = keyword_agent.extract_keywords(job_description)
        info_vars["reference_chunks"] = build_reference_chunks_str(
            retrieval_agent.retrieve(
                indexer_txt=job_summary, node_type="Project", refined_filter=False
            ),
            chunk_parser=build_highlight_str,
        )
        info_vars["previous_attempt"] = ""

        num_retries = 0
        while True:
            original_highlights = info_vars["highlights"]
            ai_assisted_highlights = enhancer_agent.step(info_vars)
            grade, remark = reviewer_agent.review(
                original_highlights, ai_assisted_highlights, job_description
            )
            info_vars["last_enhanced_version"] = ai_assisted_highlights
            info_vars["previous_attempt"] = build_previous_attempt_str(
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
