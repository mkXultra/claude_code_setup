#!/bin/bash

# Start both local and remote configurations
# This script loads both .env files and starts all services

echo "Starting both local and remote configurations..."

# Check if .env files exist
if [ ! -f ".env.local" ]; then
    echo "Warning: .env.local not found. Copying from .env.local.sample..."
    cp .env.local.sample .env.local
fi

if [ ! -f ".env.remote" ]; then
    echo "Warning: .env.remote not found. Copying from .env.remote.sample..."
    cp .env.remote.sample .env.remote
    echo "Please edit .env.remote with your remote Neo4j connection details!"
    exit 1
fi

# Start local configuration
echo "Starting local configuration..."
docker compose --env-file .env.local -f docker-compose.local.yml up -d

# Start remote configuration
echo "Starting remote configuration..."
docker compose --env-file .env.remote -f docker-compose.remote.yml up -d

echo ""
echo "Services are starting..."
echo ""
echo "Local services:"
echo "  - Neo4j Browser: http://localhost:7474"
echo "  - Neo4j Cypher MCP: http://localhost:8090"
echo "  - Graphiti MCP: http://localhost:8091"
echo ""
echo "Remote services:"
echo "  - Neo4j Cypher MCP: http://localhost:8095"
echo "  - Graphiti MCP: http://localhost:8096"
echo ""
echo "To add MCP servers to Claude Desktop:"
echo "  claude mcp add neo4j-cypher --transport sse http://localhost:8090/sse"
echo "  claude mcp add graphiti-memory --transport sse http://localhost:8091/sse"
echo "  claude mcp add remote-neo4j-cypher --transport sse http://localhost:8095/sse"
echo "  claude mcp add remote-graphiti-memory --transport sse http://localhost:8096/sse"
echo ""
echo "To view logs:"
echo "  Local: docker compose -f docker-compose.local.yml logs -f"
echo "  Remote: docker compose -f docker-compose.remote.yml logs -f"
echo "To stop: ./stop-both.sh"