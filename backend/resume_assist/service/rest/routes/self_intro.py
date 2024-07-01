from fastapi import APIRouter, HTTPException, Request, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Intro
from resume_assist.io.db.engine import neo4j_client
from resume_assist.agent_hub.summary_agent import SummaryAgent


self_intro_router = APIRouter(prefix="/self-intro", tags=["Resume: Self Introduction"])


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


@self_intro_router.post("/assist", response_model=str)
async def assist_self_intro(request: Request):
    try:
        agent = SummaryAgent("self-intro")
        info_vars = await request.json()
        ai_assisted_intro = agent.step(info_vars)
        return ai_assisted_intro
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
