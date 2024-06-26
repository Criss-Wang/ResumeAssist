import os


class Neo4jConfig:
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "admin")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "admin")
