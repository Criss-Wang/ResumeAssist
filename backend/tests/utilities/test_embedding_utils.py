import pytest
from unittest.mock import patch, Mock
from resume_assist.utilities.embedding_utils import get_indexer_embedding


@pytest.fixture
def mock_voyageai_client():
    with patch("voyageai.Client") as MockClient:
        yield MockClient


def test_get_indexer_embedding(mock_voyageai_client):
    # Arrange
    texts = ["sample text"]
    mock_embed_result = Mock()
    mock_embed_result.embeddings = [[1.0, 2.0, 3.0]]
    mock_voyageai_client.return_value.embed.return_value = mock_embed_result

    # Act
    embeddings = get_indexer_embedding(texts)

    # Assert
    assert embeddings == [[1.0, 2.0, 3.0]]
    mock_voyageai_client.return_value.embed.assert_called_once_with(
        texts, model="voyage-2", input_type="query"
    )


def test_get_indexer_embedding_empty_result(mock_voyageai_client):
    # Arrange
    texts = ["sample text"]
    mock_embed_result = Mock()
    mock_embed_result.embeddings = []
    mock_voyageai_client.return_value.embed.return_value = mock_embed_result

    # Act
    embeddings = get_indexer_embedding(texts)

    # Assert
    assert embeddings == []
    mock_voyageai_client.return_value.embed.assert_called_once_with(
        texts, model="voyage-2", input_type="query"
    )


def test_get_indexer_embedding_exception(mock_voyageai_client):
    # Arrange
    texts = ["sample text"]
    mock_voyageai_client.return_value.embed.side_effect = Exception("API error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        get_indexer_embedding(texts)

    assert str(exc_info.value) == "API error"
    mock_voyageai_client.return_value.embed.assert_called_once_with(
        texts, model="voyage-2", input_type="query"
    )
