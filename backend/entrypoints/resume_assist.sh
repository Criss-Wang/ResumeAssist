#!/bin/bash

# Start Docker Compose (go to docker folder)
cd "$(dirname "$0")/../docker"
docker-compose up -d

# Wait for Neo4j to be ready
echo "Waiting for Neo4j to be ready..."
sleep 10

cd ..

# Run FastAPI application
# resume_assist services run-rest
