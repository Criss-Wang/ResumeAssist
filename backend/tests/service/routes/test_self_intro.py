import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch, Mock
from uuid import uuid4
from resume_assist.service.rest.routes.self_intro import self_intro_router


@pytest.fixture
def mock_neo4j_client():
    with patch(
        "resume_assist.service.rest.routes.self_intro.neo4j_client"
    ) as mock_client:
        yield mock_client


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(self_intro_router)
    return TestClient(app)


@pytest.fixture
def mock_summary_agent():
    with patch(
        "resume_assist.service.rest.routes.self_intro.SummaryAgent", autospec=True
    ) as mock_agent:
        yield mock_agent


# Test case for POST /self-intro/{id}/save endpoint
def test_save_self_intro(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {"si": {"id": str(uuid4()), "content": "Introduction Content"}}
    ]
    test_id = uuid4()
    test_data = {"content": "Introduction Content"}
    response = client.post(f"/self-intro/{test_id}/save", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /self-intro/{id} endpoint
def test_get_self_intro(client, mock_neo4j_client):
    test_id = uuid4()
    test_data = {"content": "Introduction Content"}
    mock_neo4j_client.query.return_value = [{"si": test_data}]

    response = client.get(f"/self-intro/{test_id}")

    assert response.status_code == 200
    assert response.json() == test_data


# Test case for POST /self-intro/assist endpoint
def test_assist_self_intro(client, mock_summary_agent):
    mock_agent_instance = Mock()
    mock_agent_instance.step.return_value = "Assisted Introduction"
    mock_summary_agent.return_value = mock_agent_instance

    test_data = {
        "company": "some company",
        "role": "some role",
        "job_description": "some job description",
        "skills": {"category 1": ["s1", "s2"], "category 2": ["s1", "s2"]},
        "work_experiences": [
            {
                "work_company": "some work company",
                "start_date": "a start_date",
                "end_date": "a end_date",
                "work_role": "some work role",
                "highlights": ["highlight 1", "highlight 2", "highlight 3"],
            },
            {
                "work_company": "some work company",
                "start_date": "a start_date",
                "end_date": "a end_date",
                "work_role": "some work role",
                "highlights": ["highlight 1", "highlight 2", "highlight 3"],
            },
        ],
        "project_experiences": [
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
        "word_limit": 100,
    }

    response = client.post("/self-intro/assist", json=test_data)

    assert response.status_code == 200
    assert response.json() == "Assisted Introduction"
