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
        "phone": "123412432142",
        "website": "www.google.com",
    },
    "researches": [
        {"title": "fdsa", "authors": "fdsafsa", "conference": "fdsa", "date": "08/2024"}
    ],
    "educations": [
        {
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


@pytest.fixture
def resume_request():
    return ResumeRequest(
        job_details={
            "company": "Example Company",
            "position": "Software Engineer",
            "description": "Develop and maintain software applications.",
            "url": "http://www.job.com",
        },
        project_ids=[str(uuid4()) for _ in range(2)],
        work_ids=[str(uuid4()) for _ in range(2)],
        label="success",
    )


@patch("resume_assist.service.rest.routes.resume.SummaryAgent.step")
@patch("resume_assist.service.rest.routes.resume.get_indexer_embedding")
@patch("resume_assist.service.rest.routes.resume.neo4j_client")
def test_save_resume(
    mock_neo4j_client,
    mock_get_indexer_embedding,
    mock_summary_agent_step,
    resume_request,
):
    mock_summary_agent_step.return_value = "Example job summary"
    mock_get_indexer_embedding.return_value = [[0.1, 0.2, 0.3]]
    mock_neo4j_client.query.return_value = [{"r": {}}]

    response = client.post(f"/resume/{uuid4()}/save", json=resume_request.dict())

    assert response.status_code == 200
    mock_summary_agent_step.assert_called_once()
    mock_get_indexer_embedding.assert_called_once()
    mock_neo4j_client.query.assert_called_once()


@patch("resume_assist.service.rest.routes.resume.neo4j_client")
def test_get_resume(mock_neo4j_client):
    resume_id = uuid4()
    temp_data_list = [MagicMock()]
    temp_data_list[0].data.return_value = {
        "r": {"id": str(resume_id)},
        "job_details": {
            "company": "a company",
            "position": "a position",
            "description": "a description",
            "url": "http://www.job.com",
        },
        "personal_info": {
            "first_name": "a first_name",
            "last_name": "a last_name",
            "email": "a email",
            "phone": "a phone",
            "github": "a github",
            "linkedin": "a linkedin",
            "website": "a website",
        },
        "intro": {"content": "a content"},
        "skills": {
            "categories": ["cat a", "cat b"],
            "skill_mapping": '{"cat a": ["skill a1", "skill a2"], "cat b": ["skill b1", "skill b2"]}',
        },
        "works": [
            {
                "company": "a company",
                "location": "a location",
                "role": "a role",
                "start_date": "a start_date",
                "end_date": "a end_date",
                "highlights": ["highlights 1", "highlights 2", "highlights 3"],
            },
            {
                "company": "a company",
                "location": "a location",
                "role": "a role",
                "start_date": "a start_date",
                "end_date": "a end_date",
                "highlights": ["highlights 1", "highlights 2", "highlights 3"],
            },
        ],
        "projects": [
            {
                "project_name": "a project_name",
                "start_date": "a start_date",
                "end_date": "a end_date",
                "highlights": ["highlights 1", "highlights 2", "highlights 3"],
            },
            {
                "project_name": "a project_name",
                "start_date": "a start_date",
                "end_date": "a end_date",
                "highlights": ["highlights 1", "highlights 2", "highlights 3"],
            },
        ],
        "addon_info": {"keywords": ["a", "b", "c"]},
    }
    mock_neo4j_client.query.return_value = temp_data_list

    response = client.get(f"/resume/{resume_id}")

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
        MATCH (r:Resume {id: $id})
        OPTIONAL MATCH (r)-[:HAS_ADDON]->(addon_info:AddonInfo)
        OPTIONAL MATCH (r)-[:FOR_JOB]->(job_details:Job)
        OPTIONAL MATCH (r)-[:HAS_PERSONAL_INFO]->(personal_info:PersonalInfo)
        OPTIONAL MATCH (r)-[:HAS_SELF_INTRO]->(intro:SelfIntro)
        OPTIONAL MATCH (r)-[:HAS_SKILLS]->(skills:Skills)
        OPTIONAL MATCH (r)-[:HAS_PROJECT]->(pr:Project)
        OPTIONAL MATCH (r)-[:HAS_WORK]->(w:Work)
        RETURN r, addon_info, job_details, personal_info, intro, skills,
            COLLECT(DISTINCT pr) as projects,
            COLLECT(DISTINCT w) as works
        """,
        {"id": str(resume_id)},
    )


# @patch("resume_assist.service.rest.routes.resume.neo4j_client")
# def test_get_resume_not_found(mock_neo4j_client):
#     mock_neo4j_client.query.return_value = []

#     response = client.get(f"/resume/{uuid4()}")

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Full Resume not found"}
#     mock_neo4j_client.query.assert_called_once()


# @patch("resume_assist.service.rest.routes.resume.SummaryAgent.step")
# @patch("resume_assist.service.rest.routes.resume.get_indexer_embedding")
# @patch("resume_assist.service.rest.routes.resume.neo4j_client")
# def test_save_resume_error(
#     mock_neo4j_client,
#     mock_get_indexer_embedding,
#     mock_summary_agent_step,
#     resume_request,
# ):
#     mock_summary_agent_step.return_value = "Example job summary"
#     mock_get_indexer_embedding.return_value = [[0.1, 0.2, 0.3]]
#     mock_neo4j_client.query.side_effect = Exception("Database error")

#     response = client.post(f"/resume/{uuid4()}/save", json=resume_request.dict())

#     assert response.status_code == 500
#     assert response.json() == {"detail": "Unexpected error"}
#     mock_summary_agent_step.assert_called_once()
#     mock_get_indexer_embedding.assert_called_once()
#     mock_neo4j_client.query.assert_called_once()
