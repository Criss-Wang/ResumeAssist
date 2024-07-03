from fastapi import APIRouter, HTTPException, Request, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Project
from resume_assist.io.db.engine import neo4j_client
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent


project_router = APIRouter(prefix="/project", tags=["Resume: Project Experience"])


@project_router.post("/{id}/save")
def save_project(id: UUID, request: Project):
    try:
        query = """
        MERGE (pr:Project {id: $id})
        SET
            pr.project_name = $project_name,
            pr.start_date = $start_date,
            pr.end_date = $end_date,
            pr.highlights = $highlights
        RETURN pr
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


@project_router.get("/{id}", response_model=Project)
def get_project(id: UUID):
    try:
        query = """
        MATCH (pr:Project {id: $id})
        RETURN pr
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Personal Information not found")
        project = result[0]["pr"]
        return Project(**project)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@project_router.post("/assist")
async def assist_project(request: Request):
    try:
        agent = EnhancerAgent("project")
        info_vars = await request.json()
        ai_assisted_highlights = agent.step(info_vars)
        return ai_assisted_highlights
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
