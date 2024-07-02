from neo4j import GraphDatabase

from resume_assist.io.db.config import Neo4jConfig


class Neo4jClient:
    def __init__(self):
        # Create a Neo4j driver instance
        self.driver = GraphDatabase.driver(
            Neo4jConfig.NEO4J_URI,
            auth=(Neo4jConfig.NEO4J_USER, Neo4jConfig.NEO4J_PASSWORD),
        )

    def close_driver(self):
        self.driver.close()

    def query(self, query, parameters=None, db="neo4j"):
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db else self.driver.session()
            response = list(session.run(query, parameters))
        finally:
            if session is not None:
                session.close()
        return response


neo4j_client = Neo4jClient()
