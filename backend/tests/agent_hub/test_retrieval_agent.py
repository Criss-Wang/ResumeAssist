import pytest
from unittest.mock import patch
from resume_assist.agent_hub.retrieval_agent import RetrievalAgent


@pytest.fixture
def agent():
    agent = RetrievalAgent("project", use_prompt=False)
    return agent


def test_get_agent_name(agent):
    assert agent.get_agent_name() == "retriever"


@patch("resume_assist.agent_hub.retrieval_agent.get_indexer_embedding")
@patch("resume_assist.agent_hub.retrieval_agent.neo4j_client.query")
def test_step(mock_query, mock_get_indexer_embedding, agent):
    indexer_str = "sample text"
    node_type = "Job"
    indexer_embedding = [0.1, 0.2, 0.3]
    query_results = [
        {"s": {"label": "success", "content": ""}, "score": 0.9},
        {"s": {"label": "unlabeled", "content": ""}, "score": 0.8},
    ]

    mock_get_indexer_embedding.return_value = [indexer_embedding]
    mock_query.return_value = query_results

    expected_chunks = [
        ({"label": "success", "content": ""}, 0.9),
        ({"label": "unlabeled", "content": ""}, 0.8),
    ]

    result = agent.step(indexer_str, node_type)

    mock_get_indexer_embedding.assert_called_once_with([indexer_str])
    mock_query.assert_called_once()
    assert result == expected_chunks


def test_crude_filtering(agent):
    chunks = [
        ({"label": "success", "content": ""}, 0.9),
        ({"label": "unlabeled", "content": ""}, 0.8),
        ({"label": "unlabeled", "content": ""}, 0.7),
        ({"label": "success", "content": ""}, 0.6),
        ({"label": "unlabeled", "content": ""}, 0.5),
    ]
    max_chunk_size = 3
    expected_output = chunks[:max_chunk_size]

    result = agent.crude_filtering(chunks, max_chunk_size)

    assert result == expected_output


def test_rerank(agent):
    chunks = [
        ({"label": "success", "content": ""}, 0.9),
        ({"label": "unlabeled", "content": ""}, 0.8),
        ({"label": "unlabeled", "content": ""}, 0.7),
        ({"label": "success", "content": ""}, 0.6),
        ({"label": "unlabeled", "content": ""}, 0.5),
    ]
    result = agent.rerank(chunks)
    assert result == chunks


def test_refined_filtering(agent):
    chunks = [
        ({"label": "success"}, 0.9),
        ({"label": "unlabeled"}, 0.8),
        ({"label": "success"}, 0.7),
        ({"label": "unlabeled"}, 0.6),
    ]
    expected_output = [
        {"label": "success"},
        {"label": "success"},
    ]

    result = agent.refined_filtering(chunks)

    assert result == expected_output


@patch.object(RetrievalAgent, "step")
@patch.object(RetrievalAgent, "rerank")
@patch.object(RetrievalAgent, "crude_filtering")
@patch.object(RetrievalAgent, "refined_filtering")
def test_retrieve(
    mock_refined_filtering, mock_crude_filtering, mock_rerank, mock_step, agent
):
    indexer_txt = "sample text"
    node_type = "Job"
    max_chunk_size = 5
    refined_filter = True
    step_output = [
        ({"label": "success"}, 0.9),
        ({"label": "unlabeled"}, 0.8),
    ]
    rerank_output = step_output
    crude_filtering_output = step_output[:max_chunk_size]
    refined_filtering_output = [{"label": "success"}]

    mock_step.return_value = step_output
    mock_rerank.return_value = rerank_output
    mock_crude_filtering.return_value = crude_filtering_output
    mock_refined_filtering.return_value = refined_filtering_output

    expected_output = [{"label": "success"}]

    result = agent.retrieve(indexer_txt, node_type, max_chunk_size, refined_filter)

    mock_step.assert_called_once_with(indexer_txt, node_type)
    mock_rerank.assert_called_once_with(step_output)
    mock_crude_filtering.assert_called_once_with(rerank_output, max_chunk_size)
    mock_refined_filtering.assert_called_once_with(crude_filtering_output)
    assert result == expected_output

    refined_filter = False
    result = agent.retrieve(indexer_txt, node_type, max_chunk_size, refined_filter)
    assert result == crude_filtering_output
