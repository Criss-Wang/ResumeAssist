from unittest.mock import patch, MagicMock
from resume_assist.io.db.engine import Neo4jClient


@patch("resume_assist.io.db.engine.GraphDatabase")
def test_neo4j_client_init(mock_graph_database):
    mock_driver = MagicMock()
    mock_graph_database.driver.return_value = mock_driver

    client = Neo4jClient()

    mock_graph_database.driver.assert_called_once_with(
        "bolt://localhost:7687", auth=("neo4j", "neo4j_password")
    )
    assert client.driver == mock_driver


@patch("resume_assist.io.db.engine.GraphDatabase")
def test_neo4j_client_close_driver(mock_graph_database):
    mock_driver = MagicMock()
    mock_graph_database.driver.return_value = mock_driver

    client = Neo4jClient()
    client.close_driver()

    mock_driver.close.assert_called_once()


@patch("resume_assist.io.db.engine.GraphDatabase")
def test_neo4j_client_query(mock_graph_database):
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_response = [{"key": "value"}]
    mock_session.run.return_value = mock_response
    mock_driver.session.return_value = mock_session
    mock_graph_database.driver.return_value = mock_driver

    client = Neo4jClient()

    query = "MATCH (n) RETURN n"
    parameters = {"param": "value"}
    db = "neo4j"
    response = client.query(query, parameters, db)

    mock_driver.session.assert_called_once_with(database=db)
    mock_session.run.assert_called_once_with(query, parameters)
    mock_session.close.assert_called_once()
    assert response == mock_response


@patch("resume_assist.io.db.engine.GraphDatabase")
def test_neo4j_client_query_no_db(mock_graph_database):
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_response = [{"key": "value"}]
    mock_session.run.return_value = mock_response
    mock_driver.session.return_value = mock_session
    mock_graph_database.driver.return_value = mock_driver

    client = Neo4jClient()

    query = "MATCH (n) RETURN n"
    parameters = {"param": "value"}
    response = client.query(query, parameters, db=None)

    mock_driver.session.assert_called_once_with()
    mock_session.run.assert_called_once_with(query, parameters)
    mock_session.close.assert_called_once()
    assert response == mock_response
