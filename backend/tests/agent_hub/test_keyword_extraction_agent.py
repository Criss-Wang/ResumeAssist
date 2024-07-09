import pytest
from unittest.mock import Mock, patch
from resume_assist.agent_hub.keyword_extraction_agent import KeywordExtractionAgent
from resume_assist.utilities.formatting_utils import parse_to_bullet_pts


@pytest.fixture
def agent():
    agent = KeywordExtractionAgent("Project")
    agent.prompt = Mock()
    agent.prompt.system.value = "System: {job_description}"
    agent.prompt.user.value = "User: {job_description}"
    agent.engine = Mock()
    return agent


@patch("resume_assist.agent_hub.keyword_extraction_agent.parse_to_bullet_pts")
def test_ner_step(mock_parse_to_bullet_pts, agent):
    job_description = "Looking for a software engineer with experience in Python and machine learning."
    input_vars = {"job_description": job_description}
    expected_output = ["Python", "machine learning"]

    agent.engine.run_instruction = Mock(return_value=expected_output)
    mock_parse_to_bullet_pts.return_value = expected_output

    result = agent.ner_step(input_vars)

    agent.engine.run_instruction.assert_called_once()
    mock_parse_to_bullet_pts.assert_called_once_with(expected_output)
    assert result == expected_output


def test_filter(agent):
    keywords = ["Python", "machine learning", "data science", "AI", "NLP"]
    limit = 3
    expected_output = ["Python", "machine learning", "data science"]

    result = agent.filter(keywords, limit)

    assert result == expected_output


@patch.object(KeywordExtractionAgent, "ner_step")
@patch.object(KeywordExtractionAgent, "filter")
def test_extract_keywords(mock_filter, mock_ner_step, agent):
    job_description = "Looking for a software engineer with experience in Python and machine learning."
    ner_output = ["Python", "machine learning", "data science", "AI", "NLP"]
    expected_output = ["Python", "machine learning"]

    mock_ner_step.return_value = ner_output
    mock_filter.return_value = expected_output

    result = agent.extract_keywords(job_description, limit=2)

    mock_ner_step.assert_called_once_with({"job_description": job_description})
    mock_filter.assert_called_once_with(ner_output, 2)
    assert result == expected_output


def test_get_agent_name(agent):
    assert agent.get_agent_name() == "keyword_extractor"
