import pytest
import json
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from resume_assist.service.rest.routes.skills import skills_router
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent


@pytest.fixture
def mock_neo4j_client():
    with patch("resume_assist.service.rest.routes.skills.neo4j_client") as mock_client:
        yield mock_client


@pytest.fixture
def mock_enhancer_agent():
    with patch("resume_assist.service.rest.routes.skills.EnhancerAgent") as mock_agent:
        mock_instance = MagicMock(spec=EnhancerAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(skills_router)
    return TestClient(app)


# Test case for POST /skills/{id}/save endpoint
def test_save_skills(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {
            "sk": {
                "id": str(uuid4()),
                "categories": ["Category1", "Category2"],
                "skill_mapping": {"Category1": ["s1", "s2"], "Category2": ["s1", "s2"]},
            }
        }
    ]
    test_id = uuid4()
    test_data = {
        "categories": ["Category1", "Category2"],
        "skill_mapping": {"Category1": ["s1", "s2"], "Category2": ["s1", "s2"]},
    }
    response = client.post(f"/skills/{test_id}/save", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /skills/{id} endpoint
def test_get_skills(client, mock_neo4j_client):
    test_id = uuid4()
    test_data = {
        "categories": ["Category1", "Category2"],
        "skill_mapping": json.dumps(
            {"Category1": ["s1", "s2"], "Category2": ["s1", "s2"]}
        ),
    }
    mock_neo4j_client.query.return_value = [{"sk": test_data}]

    response = client.get(f"/skills/{test_id}")
    assert response.status_code == 200
    print(response.json())
    assert response.json()["skill_mapping"]["Category1"] == ["s1", "s2"]


# Test case for POST /skills/{id}/assist endpoint
def test_assist_skills(client, mock_enhancer_agent):
    return_value = ["Category1: s1,s2", "Category2: s1,s2"]
    mock_enhancer_agent.step.return_value = return_value

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
            }
        ],
        "project_experiences": [
            {
                "project_name": "a project_name",
                "start_date": "a start_date",
                "end_date": "a end_date",
                "highlights": ["highlights 1", "highlights 2", "highlights 3"],
            }
        ],
    }

    response = client.post(f"/skills/assist", json=test_data)

    assert response.status_code == 200
    assert response.json() == return_value
