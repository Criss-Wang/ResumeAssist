import pytest
import uuid
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch
from resume_assist.service.rest.routes.education import education_router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(education_router)
    return TestClient(app)


# Mocked neo4j_client
@pytest.fixture
def mock_neo4j_client():
    with patch(
        "resume_assist.service.rest.routes.education.neo4j_client", autospec=True
    ) as mock_client:
        yield mock_client


# Test case for POST /job-details/{id} endpoint
def test_save_educations(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {
            "edu": {
                "id": str(uuid.uuid4()),
                "institution": "Test institution",
                "area": "Test area",
                "degree": "Test degree",
                "gpa": "Test gpa",
                "courses": "Test courses",
                "start_date": "Test start_date",
                "end_date": "Test end_date",
                "current": False,
                "other": "other",
            }
        }
    ]
    test_id = uuid.uuid4()
    test_data = [
        {
            "institution": "Test institution",
            "area": "Test area",
            "degree": "Test degree",
            "gpa": "Test gpa",
            "courses": "Test courses",
            "start_date": "Test start_date",
            "end_date": "Test end_date",
            "current": False,
            "other": "other",
        }
    ]
    response = client.post(f"/api/education/save/{test_id}", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /job-details/{id} endpoint
def test_get_education(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "institution": "Test institution",
        "area": "Test area",
        "degree": "Test degree",
        "gpa": "Test gpa",
        "courses": "Test courses",
        "start_date": "Test start_date",
        "end_date": "Test end_date",
        "current": False,
        "other": "other",
    }
    mock_neo4j_client.query.return_value = [{"edu": test_data}]

    response = client.get(f"/api/education/{test_id}")

    assert response.status_code == 200
    assert response.json() == [test_data]
