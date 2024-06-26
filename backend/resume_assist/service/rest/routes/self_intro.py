from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import (
    IntroRequest,
    IntroResponse,
)
from resume_assist.app.enhancer_agent import EnhancerAgent


self_intro_router = APIRouter(prefix="/self-intro", tags=["resume"])


@self_intro_router.post("/{id}/save", response_model=IntroResponse)
def save_self_intro(id: UUID, request: IntroRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@self_intro_router.get("/{id}", response_model=IntroResponse)
def get_self_intro(id: UUID):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@self_intro_router.post("/{id}/assist", response_model=IntroResponse)
def assist_self_intro(id: UUID, request: IntroRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
