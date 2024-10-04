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
    resume_id = uuid.uuid4()
    education_id = uuid.uuid4()
    mock_neo4j_client.query.return_value = [
        {
            "edu": {
                "id": str(resume_id),
                "education_id": str(education_id),
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
    test_data = [
        {
            "education_id": str(education_id),
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
    response = client.post("/api/education/save", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /job-details/{id} endpoint
def test_get_education(client, mock_neo4j_client):
    education_id = uuid.uuid4()
    test_data = {
        "education_id": str(education_id),
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

    response = client.get("/api/education/all")

    assert response.status_code == 200
    assert response.json() == [test_data]
