from fastapi import APIRouter, HTTPException, Request, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Work
from resume_assist.io.db.engine import neo4j_client
from resume_assist.app.enhancer_agent import EnhancerAgent


work_experience_router = APIRouter(prefix="/work-experience", tags=["resume"])


@work_experience_router.post("/{id}/save")
def save_work_experience(id: UUID, request: Work):
    try:
        query = """
        MERGE (w:Work {id: $id})
        SET 
            w.company = $company, 
            w.location = $location, 
            w.role = $role, 
            w.start_date = $start_date, 
            w.end_date = $end_date, 
            w.highlights = $highlights
        RETURN w
        """
        parameters = {"id": str(id), **request.model_dump()}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(500, "Failed to save work experience")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@work_experience_router.get("/{id}", response_model=Work)
def get_work_experience(id: UUID):
    try:
        query = """
        MATCH (w:Work {id: $id})
        RETURN w
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Work experience not found")
        work = result[0]["w"]
        return Work(**work)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@work_experience_router.post("/assist")
async def assist_work_experience(request: Request):
    try:
        agent = EnhancerAgent("work")
        info_vars = await request.json()
        ai_assisted_highlights = agent.step(info_vars)
        return ai_assisted_highlights
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
