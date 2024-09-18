from typing import List

from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Research
from resume_assist.io.db.engine import neo4j_client


research_router = APIRouter(prefix="/api/research", tags=["Resume: Research"])


@research_router.post("/save/{id}")
def save_research(id: UUID, request: List[Research]):
    try:
        for research in request:
            query = """
            MERGE (resea:Research {id: $id})
            SET
                resea.title = $title,
                resea.authors = $authors,
                resea.conference = $conference,
                resea.date = $date
            RETURN resea
            """
            parameters = {"id": str(id), **research.model_dump()}
            result = neo4j_client.query(query, parameters)

            if not result:
                raise HTTPException(500, "Failed to save research data")

        return Response(status_code=200)
    except Exception as e:
        print(e)
        raise HTTPException(500, "Unexpected error")


@research_router.get("/{id}", response_model=List[Research])
def get_research(id: UUID):
    try:
        query = """
        MATCH (resea:Research {id: $id})
        RETURN resea
        """
        parameters = {"id": str(id)}
        result = neo4j_client.query(query, parameters)

        if not result:
            raise HTTPException(404, "No research records found")

        # Convert the query result into a list of research objects
        researchs = [Research(**record["resea"]) for record in result]

        return researchs
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
