from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import (
    PersonalInfoRequest,
    PersonalInfoResponse,
)
from resume_assist.app.enhancer_agent import EnhancerAgent


personal_info_router = APIRouter(prefix="/personal-info", tags=["resume"])


@personal_info_router.post("/{id}", response_model=PersonalInfoResponse)
def save_personal_info(id: UUID, request: PersonalInfoRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@personal_info_router.get("/{id}", response_model=PersonalInfoResponse)
def get_personal_info(id: UUID):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
