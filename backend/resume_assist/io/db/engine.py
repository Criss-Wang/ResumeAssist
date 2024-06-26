from neo4j import GraphDatabase

from resume_assist.io.db.config import Neo4jConfig


# Create a Neo4j driver instance
driver = GraphDatabase.driver(
    Neo4jConfig.NEO4J_URI, auth=(Neo4jConfig.NEO4J_USER, Neo4jConfig.NEO4J_PASSWORD)
)


def close_driver():
    driver.close()


def sample_query():
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 10")
        nodes = [record["n"] for record in result]
        return {"nodes": nodes}
