from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import JobDetails
from resume_assist.app.enhancer_agent import EnhancerAgent
from resume_assist.io.db.engine import neo4j_client


job_details_router = APIRouter(prefix="/job-details", tags=["job"])


@job_details_router.post("/{id}")
def save_job_details(id: UUID, request: JobDetails):
    try:
        query = """
        MERGE (j:Job {id: $id})
        SET j.company = $company, j.position = $position, j.description = $description, j.url = $url
        RETURN j
        """
        parameters = {
            "id": str(id),
            "company": request.company,
            "position": request.position,
            "description": request.description,
            "url": request.url,
        }
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(500, "Failed to save Job details")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@job_details_router.get("/{id}", response_model=JobDetails)
def get_job_details(id: UUID):
    try:
        query = """
        MATCH (j:Job {id: $id})
        RETURN j
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Job details not found")
        job = result[0]["j"]
        return JobDetails(**job)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
