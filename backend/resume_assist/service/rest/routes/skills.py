from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import (
    SkillsRequest,
    SkillsResponse,
)
from resume_assist.app.enhancer_agent import EnhancerAgent


skills_router = APIRouter(prefix="/skills", tags=["resume"])


@skills_router.post("/{id}/save", response_model=SkillsResponse)
def save_skills(id: UUID, request: SkillsRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@skills_router.get("/{id}", response_model=SkillsResponse)
def get_skills(id: UUID):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@skills_router.post("/{id}/assist", response_model=SkillsResponse)
def assist_skills(id: UUID, request: SkillsRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
