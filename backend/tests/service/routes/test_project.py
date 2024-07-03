import pytest
import uuid
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from resume_assist.service.rest.routes.project import project_router
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent


@pytest.fixture
def mock_neo4j_client():
    with patch("resume_assist.service.rest.routes.project.neo4j_client") as mock_client:
        yield mock_client


@pytest.fixture
def mock_enhancer_agent():
    with patch("resume_assist.service.rest.routes.project.EnhancerAgent") as mock_agent:
        mock_instance = MagicMock(spec=EnhancerAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def client():

    app = FastAPI()
    app.include_router(project_router)
    return TestClient(app)


def test_save_project(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {
            "pr": {
                "id": str(uuid.uuid4()),
                "project_name": "Project X",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "highlights": ["Achievement 1", "Achievement 2"],
            }
        }
    ]
    test_id = uuid.uuid4()
    test_data = {
        "project_name": "Project X",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "highlights": ["Achievement 1", "Achievement 2"],
    }
    response = client.post(f"/project/{test_id}/save", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /project/{id} endpoint
def test_get_project(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "project_name": "Project X",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "highlights": ["Achievement 1", "Achievement 2"],
    }
    mock_neo4j_client.query.return_value = [{"pr": test_data}]

    response = client.get(f"/project/{test_id}")

    assert response.status_code == 200
    assert response.json() == test_data


# Test case for POST /project/assist endpoint
def test_assist_project(client, mock_enhancer_agent):
    mock_enhancer_agent.step.return_value = [
        "Enhanced Highlight 1",
        "Enhanced Highlight 2",
    ]

    test_data = {
        "keywords": "some keywords",
        "highlights": ["highlight 1", "highlight 2", "highlight 3"],
    }

    response = client.post("/project/assist", json=test_data)

    assert response.status_code == 200
    assert response.json() == ["Enhanced Highlight 1", "Enhanced Highlight 2"]
