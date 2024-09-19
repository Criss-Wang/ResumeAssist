from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import PersonalInfo
from resume_assist.io.db.engine import neo4j_client


personal_info_router = APIRouter(
    prefix="/api/personal-info", tags=["Resume: Personal Information"]
)


@personal_info_router.post("/save/{id}")
def save_personal_info(id: UUID, request: PersonalInfo):
    try:
        query = """
        MERGE (pi:PersonalInfo {id: $id})
        SET
            pi.name = $name,
            pi.email = $email,
            pi.phone = $phone,
            pi.github = $github,
            pi.linkedin = $linkedin,
            pi.website = $website
        RETURN pi
        """
        parameters = {"id": str(id), **request.model_dump()}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(500, "Failed to save personal information")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@personal_info_router.get("/{id}", response_model=PersonalInfo)
def get_personal_info(id: UUID):
    try:
        query = """
        MATCH (pi:PersonalInfo {id: $id})
        RETURN pi
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Personal Information not found")
        personal_info = result[0]["pi"]
        return PersonalInfo(**personal_info)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
