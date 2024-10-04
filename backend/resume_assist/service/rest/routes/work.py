from typing import List

from fastapi import APIRouter, HTTPException, Request, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Work
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


work_experience_router = APIRouter(prefix="/api/work", tags=["Resume: Work Experience"])


@work_experience_router.post("/save")
def save_work_experience(request: List[Work]):
    try:
        for experience in request:
            query = """
            MERGE (w:Work {id: $work_id})
            SET
                w.company = $company,
                w.location = $location,
                w.role = $role,
                w.start_date = $start_date,
                w.end_date = $end_date,
                w.current = $current,
                w.highlights = $highlights
            RETURN w
            """
            parameters = {"work_id": str(experience.work_id), **experience.model_dump()}
            result = neo4j_client.query(query, parameters)
            if not result:
                raise HTTPException(500, "Failed to save work experience")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@work_experience_router.get("/all", response_model=List[Work])
def get_work_experience():
    try:
        query = """
        MATCH (w:Work)
        RETURN w
        """
        parameters = {}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Work experience not found")
        works = [Work(**record["w"]) for record in result]
        return works
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@work_experience_router.post("/assist")
async def assist_work_experience(request: Request):
    try:
        info_vars = await request.json()

        resume_info = info_vars["resume"]
        job_info = info_vars["job_details"]
        work_info = info_vars["work"]
        info_vars.update(**resume_info)
        info_vars.update(**job_info)
        info_vars.update(**work_info)

        summary_agent = SummaryAgent("work")
        keyword_agent = KeywordExtractionAgent("work")
        retrieval_agent = RetrievalAgent("work", use_prompt=False)
        enhancer_agent = EnhancerAgent("work")
        reviewer_agent = ReviewerAgent("work")

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

        enhancement_info = {}
        enhancement_info["keywords"] = str(
            keyword_agent.extract_keywords(job_description)
        )
        enhancement_info["reference_chunks"] = build_reference_chunks_str(
            retrieval_agent.retrieve(
                indexer_txt=job_summary, node_type="Work", refined_filter=False
            ),
            chunk_parser=build_highlight_str,
        )
        enhancement_info["previous_attempt"] = ""
        enhancement_info["highlights"] = info_vars["highlights"]
        enhancement_info["work_company"] = info_vars["companyName"]
        enhancement_info["work_role"] = info_vars["role"]

        num_retries = 0
        while True:
            original_highlights = info_vars["highlights"]
            # import pdb
            # pdb.set_trace()
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
