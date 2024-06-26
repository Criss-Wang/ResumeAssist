from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import (
    WorkRequest,
    WorkResponse,
)
from resume_assist.app.enhancer_agent import EnhancerAgent


work_experience_router = APIRouter(prefix="/work-experience", tags=["resume"])


@work_experience_router.post("/{id}/save", response_model=WorkResponse)
def save_work_experience(id: UUID, request: WorkRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@work_experience_router.get("/{id}", response_model=WorkResponse)
def get_work_experience(id: UUID):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@work_experience_router.post("/{id}/assist", response_model=WorkResponse)
def assist_work_experience(id: UUID, request: WorkRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
