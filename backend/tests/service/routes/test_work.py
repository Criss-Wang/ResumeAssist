import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4
from resume_assist.service.rest.routes.work import work_experience_router
from resume_assist.agent_hub.summary_agent import SummaryAgent
from resume_assist.agent_hub.keyword_extraction_agent import KeywordExtractionAgent
from resume_assist.agent_hub.retrieval_agent import RetrievalAgent
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent
from resume_assist.agent_hub.reviewer_agent import ReviewerAgent
from resume_assist.utilities.formatting_utils import (
    build_full_job_description,
)

FULL_PAYLOAD = {
    "resume": {
        "id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
        "job_details": {},
        "personal_info": {
            "name": "fda",
            "email": "fdsafas",
            "linkedin": "fdsa",
            "github": "fdsa",
            "phone": "fdsa",
            "website": "fdsa",
        },
        "researches": [
            {
                "title": "fdsa",
                "authors": "fdsafsa",
                "conference": "fdsa",
                "date": "08/2024",
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
                "end_date": "",
            }
        ],
        "self_intro": {"content": "fdafdsafds", "title": "fdsa-fdas"},
        "skills": {
            "categories": ["New Category 1"],
            "skill_mapping": {"New Category 1": ["New Skill 1", "New Skill 2"]},
        },
        "work": [
            {
                "id": 1,
                "company": "fdsa",
                "role": "df",
                "location": "fdafsa",
                "start_date": "01/2024",
                "end_date": "08/2024",
                "current": True,
                "highlights": ["new highlight"],
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
                "highlights": ["new highlight"],
            }
        ],
        "additional_info": {},
    },
    "job_details": {
        "company": "Example Company",
        "position": "Project Manager",
        "description": "Manage and oversee project execution.",
        "url": "https://test.com",
    },
    "work": {
        "id": 1,
        "companyName": "fdsa",
        "role": "df",
        "startDate": "2024-01-01T08:00:00.000Z",
        "endDate": "2024-08-01T07:00:00.000Z",
        "current": False,
        "location": "fdafsa",
        "highlights": ["Highlight 1", "Highlight 2"],
    },
}


@pytest.fixture
def mock_summary_agent():
    with patch("resume_assist.service.rest.routes.work.SummaryAgent") as mock_agent:
        mock_instance = MagicMock(spec=SummaryAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_keyword_extraction_agent():
    with patch(
        "resume_assist.service.rest.routes.work.KeywordExtractionAgent"
    ) as mock_agent:
        mock_instance = MagicMock(spec=KeywordExtractionAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_retrieval_agent():
    with patch("resume_assist.service.rest.routes.work.RetrievalAgent") as mock_agent:
        mock_instance = MagicMock(spec=RetrievalAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_enhancer_agent():
    with patch("resume_assist.service.rest.routes.work.EnhancerAgent") as mock_agent:
        mock_instance = MagicMock(spec=EnhancerAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_reviewer_agent():
    with patch("resume_assist.service.rest.routes.work.ReviewerAgent") as mock_agent:
        mock_instance = MagicMock(spec=ReviewerAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_neo4j_client():
    with patch("resume_assist.service.rest.routes.work.neo4j_client") as mock_client:
        yield mock_client


@pytest.fixture
def client():
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(work_experience_router)
    return TestClient(app)


def test_save_work_experience(mock_neo4j_client, client):
    resume_id = uuid4()
    work_id = uuid4()
    mock_neo4j_client.query.return_value = [{"w": {"id": str(work_id)}}]
    work_data = [
        {
            "id": str(resume_id),
            "work_id": str(work_id),
            "company": "Test Company",
            "location": "Test Location",
            "role": "Test Role",
            "start_date": "2022-01-01",
            "end_date": "2023-01-01",
            "current": False,
            "highlights": ["Highlight 1", "Highlight 2"],
        }
    ]

    response = client.post("/api/work/save", json=work_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.call_count == 1


def test_get_work_experience(mock_neo4j_client, client):
    work_id = uuid4()
    mock_neo4j_client.query.return_value = [
        {
            "w": {
                "work_id": str(work_id),
                "company": "Test Company",
                "location": "location",
                "role": "role",
                "start_date": "s",
                "end_date": "e",
                "current": False,
                "highlights": ["h1"],
            }
        }
    ]

    response = client.get("/api/work/all".format(id=uuid4()))

    assert response.status_code == 200
    assert response.json()[0]["company"] == "Test Company"
    assert mock_neo4j_client.query.call_count == 1


def test_assist_project(
    client,
    mock_summary_agent,
    mock_keyword_extraction_agent,
    mock_retrieval_agent,
    mock_enhancer_agent,
    mock_reviewer_agent,
):
    mock_summary_agent.step.return_value = "Example job summary"
    mock_keyword_extraction_agent.extract_keywords.return_value = [
        "keyword1",
        "keyword2",
    ]
    mock_retrieval_agent.retrieve.return_value = [
        {"highlights": ["Highlight 1", "Highlight 2"]},
        {"highlights": ["Highlight 3", "Highlight 4"]},
    ]
    mock_enhancer_agent.step.return_value = [
        "Enhanced Highlight 1",
        "Enhanced Highlight 2",
    ]
    mock_reviewer_agent.review.side_effect = [
        (4, "Bad job!"),
        (4, "Bad job!"),
        (8, "Good job!"),
    ]

    mock_request_data = FULL_PAYLOAD

    response = client.post("/api/work/assist", json=mock_request_data)

    assert response.status_code == 200
    assert response.json() == ["Enhanced Highlight 1", "Enhanced Highlight 2"]

    mock_summary_agent.step.assert_called_once_with(
        {
            "company": "Example Company",
            "role": "Project Manager",
            "job_description": "Manage and oversee project execution.",
        }
    )
    mock_keyword_extraction_agent.extract_keywords.assert_called_once_with(
        build_full_job_description(
            "Example Company",
            "Project Manager",
            "Manage and oversee project execution.",
        )
    )
    mock_retrieval_agent.retrieve.assert_called_once_with(
        indexer_txt="Example job summary", node_type="Work", refined_filter=False
    )

    mock_enhancer_agent.step.assert_any_call(
        {
            "keywords": ["keyword1", "keyword2"],
            "reference_chunks": "<Examples>\nHere are a list of examples of highlights that may be relevant to this job, use them as references points if necessary.\n\n----------\nExample 1: \n- Highlight 1\n- Highlight 2\n----------\nExample 2: \n- Highlight 3\n- Highlight 4\n\n</Examples>",
            "previous_attempt": "Here is a previous attempt to improve this highlight that failed. Learn from the remark and try to create a bettern one if possible:\n<PreviousAttempt>\n- Enhanced Highlight 1\n- Enhanced Highlight 2\n</PreviousAttempt>\n\n<Remark>\nBad job!\n</Remark>",
            "highlights": ["Highlight 1", "Highlight 2"],
            "work_company": "fdsa",
            "work_role": "df",
            "last_enhanced_version": ["Enhanced Highlight 1", "Enhanced Highlight 2"],
        }
    )
    mock_reviewer_agent.review.assert_any_call(
        ["Highlight 1", "Highlight 2"],
        ["Enhanced Highlight 1", "Enhanced Highlight 2"],
        "Company: Example Company\n----------\nRole: Project Manager\n----------\nJob Description: Manage and oversee project execution.",
    )
    mock_reviewer_agent.review.side_effect = [
        (4, "Bad job!"),
        (4, "Bad job!"),
        (4, "worst job!"),
        (4, "worst job!"),
    ]

    response = client.post("/api/work/assist", json=mock_request_data)

    assert response.status_code == 200
    assert response.json() == ["Enhanced Highlight 1", "Enhanced Highlight 2"]
