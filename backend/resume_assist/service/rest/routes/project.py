from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import (
    ProjectRequest,
    ProjectResponse,
)
from resume_assist.app.enhancer_agent import EnhancerAgent


project_router = APIRouter(prefix="/project", tags=["resume"])


@project_router.post("/{id}/save", response_model=ProjectResponse)
def save_project(id: UUID, request: ProjectRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@project_router.get("/{id}", response_model=ProjectResponse)
def get_project(id: UUID):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@project_router.post("/{id}/assist", response_model=ProjectResponse)
def assist_project(id: UUID, request: ProjectRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
