import pytest
import uuid
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from unittest.mock import patch, MagicMock
from resume_assist.service.rest.routes.project import project_router
from resume_assist.agent_hub.summary_agent import SummaryAgent
from resume_assist.agent_hub.keyword_extraction_agent import KeywordExtractionAgent
from resume_assist.agent_hub.retrieval_agent import RetrievalAgent
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent
from resume_assist.agent_hub.reviewer_agent import ReviewerAgent
from resume_assist.utilities.formatting_utils import (
    build_full_job_description,
    build_reference_chunks_str,
    build_previous_attempt_str,
    build_highlight_str,
)


@pytest.fixture
def mock_summary_agent():
    with patch("resume_assist.service.rest.routes.project.SummaryAgent") as mock_agent:
        mock_instance = MagicMock(spec=SummaryAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_keyword_extraction_agent():
    with patch(
        "resume_assist.service.rest.routes.project.KeywordExtractionAgent"
    ) as mock_agent:
        mock_instance = MagicMock(spec=KeywordExtractionAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_retrieval_agent():
    with patch(
        "resume_assist.service.rest.routes.project.RetrievalAgent"
    ) as mock_agent:
        mock_instance = MagicMock(spec=RetrievalAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_enhancer_agent():
    with patch("resume_assist.service.rest.routes.project.EnhancerAgent") as mock_agent:
        mock_instance = MagicMock(spec=EnhancerAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_reviewer_agent():
    with patch("resume_assist.service.rest.routes.project.ReviewerAgent") as mock_agent:
        mock_instance = MagicMock(spec=ReviewerAgent)
        mock_agent.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_neo4j_client():
    with patch("resume_assist.service.rest.routes.project.neo4j_client") as mock_client:
        yield mock_client


@pytest.fixture
def client():

    app = FastAPI(debug=True)
    app.include_router(project_router)
    return TestClient(app)


@pytest.fixture
def a_client():

    app = FastAPI()
    app.include_router(project_router)
    return AsyncClient(app=app, base_url="http://test")


def test_save_project(client, mock_neo4j_client):
    mock_neo4j_client.query.return_value = [
        {
            "pr": {
                "id": str(uuid.uuid4()),
                "project_name": "Project X",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "url": "some_url",
                "current": False,
                "highlights": ["Achievement 1", "Achievement 2"],
            }
        }
    ]
    test_id = uuid.uuid4()
    test_data = [
        {
            "project_name": "Project X",
            "url": "some_url",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "current": False,
            "highlights": ["Achievement 1", "Achievement 2"],
        }
    ]
    response = client.post(f"/api/project/save/{test_id}", json=test_data)

    assert response.status_code == 200
    assert mock_neo4j_client.query.called


# Test case for GET /project/{id} endpoint
def test_get_project(client, mock_neo4j_client):
    test_id = uuid.uuid4()
    test_data = {
        "project_name": "Project X",
        "url": "some_url",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "current": False,
        "highlights": ["Achievement 1", "Achievement 2"],
    }

    mock_neo4j_client.query.return_value = [{"pr": test_data}]

    response = client.get(f"/api/project/{test_id}")

    assert response.status_code == 200
    assert response.json() == [test_data]


# Test case for POST /project/assist endpoint
# @pytest.mark.anyio
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

    mock_request_data = {
        "resume": {},
        "job_details": {
            "company": "Example Company",
            "position": "Project Manager",
            "description": "Manage and oversee project execution.",
            "url": "https://test.com",
        },
        "project": {
            "project_name": "Project X",
            "url": "some_url",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "current": False,
            "highlights": ["Highlight 1", "Highlight 2"],
        },
    }

    response = client.post("/api/project/assist", json=mock_request_data)

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
        indexer_txt="Example job summary", node_type="Project", refined_filter=False
    )

    mock_enhancer_agent.step.assert_any_call(
        {
            "keywords": ["keyword1", "keyword2"],
            "reference_chunks": "<Examples>\nHere are a list of examples of highlights that may be relevant to this job, use them as references points if necessary.\n\n----------\nExample 1: \n- Highlight 1\n- Highlight 2\n----------\nExample 2: \n- Highlight 3\n- Highlight 4\n\n</Examples>",
            "previous_attempt": "Here is a previous attempt to improve this highlight that failed. Learn from the remark and try to create a bettern one if possible:\n<PreviousAttempt>\n- Enhanced Highlight 1\n- Enhanced Highlight 2\n</PreviousAttempt>\n\n<Remark>\nBad job!\n</Remark>",
            "highlights": ["Highlight 1", "Highlight 2"],
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

    response = client.post("/api/project/assist", json=mock_request_data)

    assert response.status_code == 200
    assert response.json() == ["Enhanced Highlight 1", "Enhanced Highlight 2"]
