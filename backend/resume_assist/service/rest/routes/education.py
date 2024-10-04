from typing import List

from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Education
from resume_assist.io.db.engine import neo4j_client


education_router = APIRouter(prefix="/api/education", tags=["Resume: Education"])


@education_router.post("/save")
def save_education(request: List[Education]):
    try:
        for education in request:
            query = """
            MERGE (edu:Education {id: $education_id})
            SET
                edu.institution = $institution,
                edu.area = $area,
                edu.degree = $degree,
                edu.gpa = $gpa,
                edu.courses = $courses,
                edu.current = $current,
                edu.start_date = $start_date,
                edu.end_date = $end_date,
                edu.other = $other
            RETURN edu
            """
            parameters = {
                "education_id": str(education.education_id),
                **education.model_dump(),
            }
            result = neo4j_client.query(query, parameters)

            if not result:
                raise HTTPException(500, "Failed to save education data")

        return Response(status_code=200)
    except Exception as e:
        print(e)
        raise HTTPException(500, "Unexpected error")


@education_router.get("/all", response_model=List[Education])
def get_education():
    try:
        query = """
        MATCH (edu:Education)
        RETURN edu
        """
        parameters = {}
        result = neo4j_client.query(query, parameters)

        if not result:
            raise HTTPException(404, "No education records found")

        # Convert the query result into a list of Education objects
        educations = [Education(**record["edu"]) for record in result]

        return educations
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")
