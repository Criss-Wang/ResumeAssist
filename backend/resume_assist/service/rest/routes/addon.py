from fastapi import APIRouter, HTTPException
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import (
    AddonRequest,
    AddonResponse,
)
from resume_assist.app.enhancer_agent import EnhancerAgent


addon_info_router = APIRouter(prefix="/addon", tags=["resume"])


@addon_info_router.post("/{id}", response_model=AddonResponse)
def save_addon_info(id: UUID, request: AddonRequest):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@addon_info_router.get("/{id}", response_model=AddonResponse)
def get_addon_info(id: UUID):  # /1?q=somequery
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
