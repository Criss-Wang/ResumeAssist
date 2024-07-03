from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import AddonInfo
from resume_assist.io.db.engine import neo4j_client


addon_info_router = APIRouter(prefix="/addon", tags=["Resume: Addon Information"])


@addon_info_router.post("/{id}")
def save_addon_info(id: UUID, request: AddonInfo):
    try:
        query = """
        MERGE (ao:AddonInfo {id: $id})
        SET
            ao.keywords = $keywords
        RETURN ao
        """
        parameters = {"id": str(id), **request.model_dump()}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(500, "Failed to save additional information")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@addon_info_router.get("/{id}", response_model=AddonInfo)
def get_addon_info(id: UUID):  # /1?q=somequery
    try:
        query = """
        MATCH (ao:AddonInfo {id: $id})
        RETURN ao
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Additional Info not found")
        work = result[0]["ao"]
        return AddonInfo(**work)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
