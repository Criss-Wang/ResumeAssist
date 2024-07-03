import pytest
import uuid
from fastapi.testclient import TestClient
from resume_assist.service.rest.routes.addon import addon_info_router
from resume_assist.io.db.engine import neo4j_client


@pytest.fixture
def client():
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(addon_info_router)
    return TestClient(app)


def test_save_addon_info(client):
    test_id = uuid.uuid4()
    test_data = {"keywords": ["python", "fastapi", "neo4j"]}
    response = client.post(f"/addon/{test_id}", json=test_data)

    assert response.status_code == 200
    assert (
        neo4j_client.query(f"MATCH (ao:AddonInfo {{id: '{test_id}'}}) RETURN ao")
        is not None
    )


# Test case for GET /addon/{id} endpoint
def test_get_addon_info(client):
    test_id = uuid.uuid4()
    test_data = {"keywords": ["python", "fastapi", "neo4j"]}
    # Save test data to Neo4j
    neo4j_client.query(
        "CREATE (ao:AddonInfo {id: $id, keywords: $keywords})",
        {"id": str(test_id), "keywords": test_data["keywords"]},
    )

    response = client.get(f"/addon/{test_id}")

    assert response.status_code == 200
    assert response.json()["keywords"] == test_data["keywords"]
