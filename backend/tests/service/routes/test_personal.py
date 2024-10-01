import pytest
import uuid
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch
from resume_assist.service.rest.routes.personal import personal_info_router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(personal_info_router)
    return TestClient(app)


# Mocked neo4j_client
@pytest.fixture
def mock_neo4j_client():
    with patch(
        "resume_assist.service.rest.routes.personal.neo4j_client", autospec=True
    ) as mock_client:
        yield mock_client


# Test case for POST /personal-info/{id} endpoint
def test_save_personal_info(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {
            "pi": {
                "id": str(uuid.uuid4()),
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "123456789",
                "github": "johndoe",
                "linkedin": "johndoe",
                "website": "https://johndoe.com",
            }
        }
    ]
    test_id = uuid.uuid4()
    test_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "github": "johndoe",
        "linkedin": "johndoe",
        "website": "https://johndoe.com",
    }
    response = client.post(f"/api/personal-info/save/{test_id}", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /personal-info/{id} endpoint
def test_get_personal_info(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "github": "johndoe",
        "linkedin": "johndoe",
        "website": "https://johndoe.com",
    }
    mock_neo4j_client.query.return_value = [{"pi": test_data}]

    response = client.get(f"/api/personal-info/{test_id}")

    assert response.status_code == 200
    assert response.json() == test_data
