import pytest
import uuid
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch
from resume_assist.service.rest.routes.research import research_router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(research_router)
    return TestClient(app)


# Mocked neo4j_client
@pytest.fixture
def mock_neo4j_client():
    with patch(
        "resume_assist.service.rest.routes.research.neo4j_client", autospec=True
    ) as mock_client:
        yield mock_client


def test_save_research(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    mock_neo4j_client.query.return_value = [
        {
            "resea": {
                "id": str(test_id),
                "title": "Test title",
                "authors": "Test authors",
                "conference": "Test conference",
                "date": "Test date",
            }
        }
    ]
    test_data = [
        {
            "title": "Test title",
            "authors": "Test authors",
            "conference": "Test conference",
            "date": "Test date",
        }
    ]
    response = client.post(f"/api/research/save/{test_id}", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /job-details/{id} endpoint
def test_get_research(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "title": "Test title",
        "authors": "Test authors",
        "conference": "Test conference",
        "date": "Test date",
    }
    mock_neo4j_client.query.return_value = [{"resea": test_data}]

    response = client.get(f"/api/research/{test_id}")

    assert response.status_code == 200
    assert response.json() == [test_data]
