import pytest
from unittest.mock import patch, MagicMock
from resume_assist.engines.base_engine import BaseEngine
from resume_assist.agent_hub.reviewer_agent import ReviewerAgent


@pytest.fixture
def agent():
    agent = ReviewerAgent("project")
    return agent


def test_get_agent_name(agent):
    assert agent.get_agent_name() == "reviewer"


@patch("resume_assist.agent_hub.reviewer_agent.parse_grading_details")
@patch("resume_assist.agent_hub.base.load_engine")
def test_grade(mock_load_engine, mock_parse_grading_details):
    mock_engine_instance = MagicMock(spec=BaseEngine)
    mock_engine_instance.run_instruction.return_value = "mock output"
    mock_load_engine.return_value = lambda params, name: mock_engine_instance
    mock_parse_grading_details.return_value = (10, "Excellent improvement")

    input_vars = {
        "original_content": ["original content"],
        "improved_content": ["improved content"],
        "job_description": "job description",
    }
    system_prompt = "System prompt with {original_content}, {improved_content}, and {job_description}"
    user_prompt = (
        "User prompt with {original_content}, {improved_content}, and {job_description}"
    )
    expected_messages = [
        ("system", system_prompt.format(**input_vars)),
        ("user", user_prompt.format(**input_vars)),
    ]
    agent = ReviewerAgent("project")
    agent.prompt.system.value = system_prompt
    agent.prompt.user.value = user_prompt
    result = agent.grade(input_vars)

    mock_engine_instance.run_instruction.assert_called_once_with(expected_messages)
    mock_parse_grading_details.assert_called_once_with("mock output")
    assert result == (10, "Excellent improvement")


@patch.object(ReviewerAgent, "grade")
def test_review(mock_grade, agent):
    original_content = ["original content"]
    improved_content = ["improved content"]
    job_description = "job description"
    mock_grade.return_value = (10, "Excellent improvement")

    result = agent.review(original_content, improved_content, job_description)

    mock_grade.assert_called_once_with(
        {
            "original_content": original_content,
            "improved_content": improved_content,
            "job_description": job_description,
        }
    )
    assert result == (10, "Excellent improvement")
