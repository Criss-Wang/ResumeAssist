import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Response

from resume_assist.service.rest.data_model.resume_model import Skills
from resume_assist.io.db.engine import neo4j_client
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent


skills_router = APIRouter(prefix="/skills", tags=["Resume: Skills"])


@skills_router.post("/{id}/save")
def save_skills(id: UUID, request: Skills):
    try:
        query = """
        MERGE (sk:Skills {id: $id})
        SET sk.categories = $categories, sk.skill_mapping = $skill_mapping
        RETURN sk
        """
        parameters = {
            "id": str(id),
            "categories": request.categories,
            "skill_mapping": json.dumps(request.skill_mapping),
        }
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(500, "Failed to save skills")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@skills_router.get("/{id}", response_model=Skills)
def get_skills(id: UUID):
    try:
        query = """
        MATCH (sk:Skills {id: $id})
        RETURN sk
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Self Introduction not found")
        skills = result[0]["sk"]
        return Skills(
            categories=skills.get("categories"),
            skill_mapping=json.loads(skills.get("skill_mapping")),
        )
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@skills_router.post("/{id}/assist", response_model=Skills)
def assist_skills(id: UUID, request: Skills):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
