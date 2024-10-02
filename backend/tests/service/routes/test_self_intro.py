import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch, Mock
from uuid import uuid4
from resume_assist.service.rest.routes.self_intro import self_intro_router


@pytest.fixture
def mock_neo4j_client():
    with patch(
        "resume_assist.service.rest.routes.self_intro.neo4j_client"
    ) as mock_client:
        yield mock_client


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(self_intro_router)
    return TestClient(app)


@pytest.fixture
def mock_summary_agent():
    with patch(
        "resume_assist.service.rest.routes.self_intro.SummaryAgent", autospec=True
    ) as mock_agent:
        yield mock_agent


# Test case for POST /self-intro/{id}/save endpoint
def test_save_self_intro(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {
            "si": {
                "title": "test title",
                "content": "Introduction Content",
            }
        }
    ]
    test_id = str(uuid4())
    test_data = {"title": "test title", "content": "Introduction Content"}
    response = client.post(f"/api/self-intro/save/{test_id}", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /self-intro/{id} endpoint
def test_get_self_intro(client, mock_neo4j_client):
    test_data = {"title": "test title", "content": "Introduction Content"}
    mock_neo4j_client.query.return_value = [{"si": test_data}]

    response = client.get(f"/api/self-intro/all")

    assert response.status_code == 200
    assert response.json() == [test_data]


# Test case for POST /self-intro/assist endpoint
def test_assist_self_intro(client, mock_summary_agent):
    mock_agent_instance = Mock()
    mock_agent_instance.step.return_value = "Assisted Introduction"
    mock_summary_agent.return_value = mock_agent_instance

    test_data = {
        "resume": {
            "id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
            "job_details": {
                "position": "fdas",
                "company": "fdsa",
                "url": "fdas",
                "description": "fasfdsadf"
            },
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
        "intro": {
            "content": "fdafdsafds",
            "title": "fdsa-fdas"
        }
    }

    response = client.post("/api/self-intro/assist", json=test_data)

    assert response.status_code == 200
    assert response.json() == "Assisted Introduction"
