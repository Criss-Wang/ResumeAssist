from typing import List

from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Research
from resume_assist.io.db.engine import neo4j_client


research_router = APIRouter(prefix="/api/research", tags=["Resume: Research"])


@research_router.post("/save")
def save_research(request: List[Research]):
    try:
        for research in request:
            query = """
            MERGE (resea:Research {id: $research_id})
            SET
                resea.title = $title,
                resea.authors = $authors,
                resea.conference = $conference,
                resea.date = $date
            RETURN resea
            """
            parameters = {
                "research_id": str(research.research_id),
                **research.model_dump(),
            }
            result = neo4j_client.query(query, parameters)

            if not result:
                raise HTTPException(500, "Failed to save research data")

        return Response(status_code=200)
    except Exception as e:
        print(e)
        raise HTTPException(500, "Unexpected error")


@research_router.get("/all", response_model=List[Research])
def get_research():
    try:
        query = """
        MATCH (resea:Research)
        RETURN resea
        """
        parameters = {}
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
