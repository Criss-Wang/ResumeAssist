from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import (
    JobDetailsRequest,
    JobDetailsResponse,
)
from resume_assist.app.enhancer_agent import EnhancerAgent


job_details_router = APIRouter(prefix="/job-details", tags=["job"])


@job_details_router.post("/{id}", response_model=JobDetailsResponse)
def save_job_details(id: UUID, request: JobDetailsRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@job_details_router.get("/{id}", response_model=JobDetailsResponse)
def get_job_details(id: UUID):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
