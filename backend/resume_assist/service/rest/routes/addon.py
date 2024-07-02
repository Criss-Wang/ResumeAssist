from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import AddonInfo
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent


addon_info_router = APIRouter(prefix="/addon", tags=["Resume: Addon Information"])


@addon_info_router.post("/{id}")
def save_addon_info(id: UUID, request: AddonInfo):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@addon_info_router.get("/{id}", response_model=AddonInfo)
def get_addon_info(id: UUID):  # /1?q=somequery
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
