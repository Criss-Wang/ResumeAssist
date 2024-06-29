from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Intro
from resume_assist.io.db.engine import neo4j_client
from resume_assist.app.enhancer_agent import EnhancerAgent


self_intro_router = APIRouter(prefix="/self-intro", tags=["resume"])


@self_intro_router.post("/{id}/save")
def save_self_intro(id: UUID, request: Intro):
    try:
        query = """
        MERGE (si:SelfIntro {id: $id})
        SET si.content = $content
        RETURN si
        """
        parameters = {
            "id": str(id),
            "content": request.content,
        }
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(500, "Failed to save self introduction")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@self_intro_router.get("/{id}", response_model=Intro)
def get_self_intro(id: UUID):
    try:
        query = """
        MATCH (si:SelfIntro {id: $id})
        RETURN si
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Self Introduction not found")
        self_intro = result[0]["si"]
        return Intro(**self_intro)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@self_intro_router.post("/{id}/assist", response_model=Intro)
def assist_self_intro(id: UUID, request: Intro):
    try:
        pass
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
