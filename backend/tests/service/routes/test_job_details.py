import pytest
import uuid
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch
from resume_assist.service.rest.routes.job_details import job_details_router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(job_details_router)
    return TestClient(app)


# Mocked neo4j_client
@pytest.fixture
def mock_neo4j_client():
    with patch(
        "resume_assist.service.rest.routes.job_details.neo4j_client", autospec=True
    ) as mock_client:
        yield mock_client


# Test case for POST /job-details/{id} endpoint
def test_save_job_details(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {
            "j": {
                "id": str(uuid.uuid4()),
                "company": "Test Company",
                "position": "Test Position",
                "description": "Test Description",
                "url": "https://test.com",
            }
        }
    ]
    test_id = uuid.uuid4()
    test_data = {
        "company": "Test Company",
        "position": "Test Position",
        "description": "Test Description",
        "url": "https://test.com",
    }
    response = client.post(f"/job-details/{test_id}", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /job-details/{id} endpoint
def test_get_job_details(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "company": "Test Company",
        "position": "Test Position",
        "description": "Test Description",
        "url": "https://test.com",
    }
    mock_neo4j_client.query.return_value = [{"j": test_data}]

    response = client.get(f"/job-details/{test_id}")

    assert response.status_code == 200
    assert response.json() == test_data
