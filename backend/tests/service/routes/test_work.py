import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4
from resume_assist.service.rest.routes.work import work_experience_router
from resume_assist.service.rest.data_model.resume_model import Work
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent


@pytest.fixture
def mock_neo4j_client():
    with patch("resume_assist.service.rest.routes.work.neo4j_client") as mock_client:
        yield mock_client


@pytest.fixture
def mock_enhancer_agent():
    with patch("resume_assist.service.rest.routes.work.EnhancerAgent") as mock_agent:
        mock_instance = MagicMock(spec=EnhancerAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def test_client():
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(work_experience_router)
    return TestClient(app)


def test_save_work_experience(mock_neo4j_client, test_client):
    mock_neo4j_client.query.return_value = [{"w": {"id": str(uuid4())}}]

    work_data = {
        "company": "Test Company",
        "location": "Test Location",
        "role": "Test Role",
        "start_date": "2022-01-01",
        "end_date": "2023-01-01",
        "highlights": ["Highlight 1", "Highlight 2"],
    }

    response = test_client.post(
        "/work-experience/{id}/save".format(id=uuid4()), json=work_data
    )

    assert response.status_code == 200
    assert mock_neo4j_client.query.call_count == 1


def test_get_work_experience(mock_neo4j_client, test_client):
    mock_neo4j_client.query.return_value = [
        {
            "w": {
                "id": str(uuid4()),
                "company": "Test Company",
                "location": "location",
                "role": "role",
                "start_date": "s",
                "end_date": "e",
                "highlights": ["h1"],
            }
        }
    ]

    response = test_client.get("/work-experience/{id}".format(id=uuid4()))

    assert response.status_code == 200
    assert response.json()["company"] == "Test Company"
    assert mock_neo4j_client.query.call_count == 1


def test_assist_work_experience(mock_enhancer_agent, test_client):
    mock_response = ["AI Highlight 1", "AI Highlight 2"]
    mock_enhancer_agent.step.return_value = mock_response

    info_vars = {
        "company": "some company",
        "role": "some role",
        "job_description": "some job description",
        "keywords": "some keywords",
        "work_company": "some work company",
        "work_role": "some work role",
        "highlights": ["highlight 1", "highlight 2", "highlight 3"],
    }

    response = test_client.post("/work-experience/assist", json=info_vars)

    assert response.status_code == 200
    assert response.json() == ["AI Highlight 1", "AI Highlight 2"]
    mock_enhancer_agent.step.assert_called_once_with(info_vars)
