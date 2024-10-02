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
    response = client.post(f"/api/skills/save/{test_id}", json=test_data)

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

    response = client.get(f"/api/skills/{test_id}")
    assert response.status_code == 200
    print(response.json())
    assert response.json()["skill_mapping"]["Category1"] == ["s1", "s2"]


# Test case for POST /skills/{id}/assist endpoint
def test_assist_skills(client, mock_enhancer_agent):
    return_value = ["Category1: s1,s2", "Category2: s1,s2"]
    mock_enhancer_agent.step.return_value = return_value

    test_data = {
        "resume": {
            "id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
            "job_details": {},
            "personal_info": {
                "name": "fda",
                "email": "fdsafas",
                "linkedin": "fdsa",
                "github": "fdsa",
                "phone": "fdsa",
                "website": "fdsa"
            },
            "researches": [
                {
                    "title": "fdsa",
                    "authors": "fdsafsa",
                    "conference": "fdsa",
                    "date": "08/2024"
                }
            ],
            "educations": [
                {
                    "institution": "fda",
                    "area": "fdsafsadf",
                    "degree": "dadsafdsaf",
                    "current": True,
                    "gpa": "fdsafdsa",
                    "courses": "fdafsaf",
                    "other": "fdsafas;fdsafdsafafdsa",
                    "start_date": "07/2024",
                    "end_date": ""
                }
            ],
            "self_intro": {
                "content": "fdafdsafds",
                "title": "fdsa-fdas"
            },
            "skills": {
                "categories": [
                    "New Category 1"
                ],
                "skill_mapping": {
                    "New Category 1": [
                        "New Skill 1",
                        "New Skill 2"
                    ]
                }
            },
            "work": [
                {
                    "id": 1,
                    "company": "fdsa",
                    "role": "df",
                    "location": "fdafsa",
                    "start_date": "01/2024",
                    "end_date": "08/2024",
                    "current": False,
                    "highlights": [
                        "new highlight"
                    ]
                }
            ],
            "projects": [
                {
                    "id": 1,
                    "project_name": "llm-benchmark",
                    "start_date": "Invalid Date",
                    "end_date": "",
                    "url": "fdsafsa",
                    "current": True,
                    "highlights": [
                        "new highlight"
                    ]
                }
            ],
            "additional_info": {}
        },
        "job": {
            "position": "fdas",
            "company": "fdsa",
            "url": "fdas",
            "description": "fasfdsadf"
        },
        "categories": [
            {
                "name": "New Category 1",
                "skills": [
                    {
                        "name": "New Skill 1",
                        "catName": "New Category 1"
                    },
                    {
                        "name": "New Skill 2",
                        "catName": "New Category 1"
                    }
                ]
            }
        ]
    }

    response = client.post("/api/skills/assist", json=test_data)

    assert response.status_code == 200
    assert response.json() == return_value
