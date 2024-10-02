from typing import List

from fastapi import APIRouter, HTTPException, Request, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Intro
from resume_assist.io.db.engine import neo4j_client
from resume_assist.agent_hub.summary_agent import SummaryAgent


self_intro_router = APIRouter(
    prefix="/api/self-intro", tags=["Resume: Self Introduction"]
)


@self_intro_router.post("/save/{id}")
def save_self_intro(id: UUID, request: Intro):
    try:
        query = """
        MERGE (si:SelfIntro {id: $id})
        SET si.content = $content,
            si.title = $title
        RETURN si
        """
        result = neo4j_client.query(query, {"id": str(id), **request.model_dump()})
        if not result:
            raise HTTPException(500, "Failed to save self introduction")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@self_intro_router.post("/assist", response_model=str)
async def assist_self_intro(request: Request):
    try:
        agent = SummaryAgent("self-intro")
        info_vars = await request.json()

        intro_vars = {}
        intro_vars.update(**info_vars["intro"])
        intro_vars.update(**info_vars["resume"]["job_details"])
        intro_vars["skills"] = info_vars["resume"]["skills"]
        intro_vars["work_experiences"] = info_vars["resume"]["work"]
        intro_vars["project_experiences"] = info_vars["resume"]["projects"]
        ai_assisted_intro = agent.step(intro_vars)
        return ai_assisted_intro
    except Exception as e:
        print(e)
        raise HTTPException(500, "Unexpected error")


# @self_intro_router.post("/{id}", response_model=Intro)
# def get_self_intro(id: UUID):
#     try:
#         query = """
#         MATCH (si:SelfIntro {id: $id})
#         RETURN si
#         """
#         parameters = {"id": str(id)}
#         result = neo4j_client.query(query, parameters)
#         if not result:
#             raise HTTPException(404, "Self Introduction not found")
#         self_intro = result[0]["si"]
#         return Intro(**self_intro)
#     except Exception as e:
#         # logger.exception(e)
#         print(e)
#         raise HTTPException(500, "Unexpected error")


@self_intro_router.get("/all", response_model=List[Intro])
def get_self_intro_all():
    try:
        query = """
        MATCH (si:SelfIntro)
        RETURN si
        """
        result = neo4j_client.query(query)
        if not result:
            print("no existing self intro, check your database")
        # Convert the result to a list of Intro objects
        self_intros = [Intro(**record["si"]) for record in result]

        return self_intros
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
