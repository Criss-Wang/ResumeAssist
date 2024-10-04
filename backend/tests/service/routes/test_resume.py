import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock
from uuid import uuid4

from resume_assist.service.rest.data_model.resume_model import ResumeRequest
from resume_assist.service.rest.routes.resume import resume_router

client = TestClient(resume_router)

FULL_PAYLOAD = {
    "id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
    "job_details": {
        "position": "fdas",
        "company": "fdsa",
        "url": "fdas",
        "description": "fasfdsadf",
    },
    "personal_info": {
        "name": "fda",
        "email": "test@test.com",
        "linkedin": "https://www.linkedin.com/in/zhenlin-wang/",
        "github": "https://github.com/Criss-Wang",
        "phone": "+86 13900000000",
        "website": "www.google.com",
    },
    "researches": [
        {
            "research_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
            "title": "fdsa",
            "authors": "fdsafsa",
            "conference": "fdsa",
            "date": "08/2024",
        }
    ],
    "educations": [
        {
            "education_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
            "institution": "fda",
            "area": "fdsafsadf",
            "degree": "dadsafdsaf",
            "current": True,
            "gpa": "fdsafdsa",
            "courses": "fdafsaf",
            "other": "fdsafas;fdsafdsafafdsa",
            "start_date": "07/2024",
            "end_date": "",
        }
    ],
    "self_intro": {"content": "fdafdsafds", "title": "fdsa-fdas"},
    "skills": {
        "categories": ["New Category 1"],
        "skill_mapping": {"New Category 1": ["New Skill 1", "New Skill 2"]},
    },
    "work": [
        {
            "id": 1,
            "work_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
            "company": "fdsa",
            "role": "df",
            "location": "fdafsa",
            "start_date": "01/2024",
            "end_date": "08/2024",
            "current": False,
            "highlights": ["new highlight"],
        }
    ],
    "projects": [
        {
            "id": 1,
            "project_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
            "project_name": "llm-benchmark",
            "start_date": "Invalid Date",
            "end_date": "",
            "url": "fdsafsa",
            "current": True,
            "highlights": ["new highlight"],
        }
    ],
    "additional_info": {},
}


@patch("resume_assist.service.rest.routes.resume.SummaryAgent.step")
@patch("resume_assist.service.rest.routes.resume.get_indexer_embedding")
@patch("resume_assist.service.rest.routes.resume.neo4j_client")
def test_save_resume(
    mock_neo4j_client,
    mock_get_indexer_embedding,
    mock_summary_agent_step,
):
    mock_summary_agent_step.return_value = "Example job summary"
    mock_get_indexer_embedding.return_value = [[0.1, 0.2, 0.3]]
    mock_neo4j_client.query.return_value = [{"r": {}}]

    info_vars = FULL_PAYLOAD

    response = client.post(f"/api/resume/save/{uuid4()}", json=info_vars)

    assert response.status_code == 200
    mock_summary_agent_step.assert_called_once()
    mock_get_indexer_embedding.assert_called_once()
    mock_neo4j_client.query.assert_called_once()

    info_vars["label"] = "success"
    response = client.post(f"/api/resume/save/{uuid4()}", json=info_vars)

    assert response.status_code == 200


@patch("resume_assist.service.rest.routes.resume.neo4j_client")
def test_get_resume(mock_neo4j_client):
    resume_id = uuid4()
    temp_data_list = [MagicMock()]
    temp_data_list[0].data.return_value = {
        "id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
        "job_details": {
            "position": "fdas",
            "company": "fdsa",
            "url": "fdas",
            "description": "fasfdsadf",
        },
        "personal_info": {
            "name": "fda",
            "email": "test@test.com",
            "linkedin": "https://www.linkedin.com/in/zhenlin-wang/",
            "github": "https://github.com/Criss-Wang",
            "phone": "+86 13900000000",
            "website": "www.google.com",
        },
        "researches": [
            {
                "research_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
                "title": "fdsa",
                "authors": "fdsafsa",
                "conference": "fdsa",
                "date": "08/2024",
            }
        ],
        "educations": [
            {
                "education_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
                "institution": "fda",
                "area": "fdsafsadf",
                "degree": "dadsafdsaf",
                "current": True,
                "gpa": "fdsafdsa",
                "courses": "fdafsaf",
                "other": "fdsafas;fdsafdsafafdsa",
                "start_date": "07/2024",
                "end_date": "",
            }
        ],
        "self_intro": {"content": "fdafdsafds", "title": "fdsa-fdas"},
        "skills": {
            "categories": ["cat a", "cat b"],
            "skill_mapping": '{"cat a": ["skill a1", "skill a2"], "cat b": ["skill b1", "skill b2"]}',
        },
        "work": [
            {
                "id": 1,
                "work_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
                "company": "fdsa",
                "role": "df",
                "location": "fdafsa",
                "start_date": "01/2024",
                "end_date": "08/2024",
                "current": False,
                "highlights": ["new highlight"],
            }
        ],
        "projects": [
            {
                "id": 1,
                "project_id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
                "project_name": "llm-benchmark",
                "start_date": "Invalid Date",
                "end_date": "",
                "url": "fdsafsa",
                "current": True,
                "highlights": ["new highlight"],
            }
        ],
        "label": "success",
    }
    mock_neo4j_client.query.return_value = temp_data_list

    response = client.get(f"/api/resume/{resume_id}")

    assert response.status_code == 200
    resume_data = response.json()
    assert resume_data["skills"] == {
        "categories": ["cat a", "cat b"],
        "skill_mapping": {
            "cat a": ["skill a1", "skill a2"],
            "cat b": ["skill b1", "skill b2"],
        },
    }

    mock_neo4j_client.query.assert_called_once_with(
        """
        MATCH (r:Resume {id: $resume_id})
        OPTIONAL MATCH (r)-[:FOR_JOB]->(job_details:Job)
        OPTIONAL MATCH (r)-[:HAS_PERSONAL_INFO]->(personal_info:PersonalInfo)
        OPTIONAL MATCH (r)-[:HAS_SELF_INTRO]->(intro:SelfIntro)
        OPTIONAL MATCH (r)-[:HAS_SKILLS]->(skills:Skills)
        OPTIONAL MATCH (r)-[:HAS_PROJECT]->(pr:Project)
        OPTIONAL MATCH (r)-[:HAS_WORK]->(w:Work)
        OPTIONAL MATCH (r)-[:HAS_EDUCATION]->(edu:Education)
        OPTIONAL MATCH (r)-[:HAS_RESEARCH]->(resea:Research)
        RETURN r, job_details, personal_info, intro, skills,
            COLLECT(DISTINCT pr) as projects,
            COLLECT(DISTINCT w) as work,
            COLLECT(DISTINCT edu) as educations,
            COLLECT(DISTINCT resea) as researches,
        """,
        {"resume_id": str(resume_id)},
    )
