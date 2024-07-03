import uuid
import pytest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from resume_assist.service.rest.routes.addon import addon_info_router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(addon_info_router)
    return TestClient(app)


# Mocked neo4j_client
@pytest.fixture
def mock_neo4j_client():
    with patch(
        "resume_assist.service.rest.routes.addon.neo4j_client", autospec=True
    ) as mock_client:
        yield mock_client


# Test case for POST /addon/{id} endpoint
def test_save_addon_info(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "keywords": ["k1", "k2"],
    }
    response = client.post(f"/addon/{test_id}", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /addon/{id} endpoint
def test_get_addon_info(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "keywords": ["k1", "k2"],
    }
    mock_neo4j_client.query.return_value = [{"ao": test_data}]

    response = client.get(f"/addon/{test_id}")

    assert response.status_code == 200
    assert response.json() == test_data
