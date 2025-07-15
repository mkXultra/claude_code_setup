# Memory MCP Setup

This project provides a Docker Compose setup for running Neo4j with MCP (Model Context Protocol) servers for graph-based memory management.

## Services

- **Neo4j**: Graph database for storing memory data
- **mcp-neo4j-cypher-server**: MCP server for executing Cypher queries
- **graphiti-mcp**: MCP server for managing memory in Neo4j

## Quick Start

### Option 1: Local Neo4j Database

1. Copy the environment file sample:
```bash
cp .env.local.sample .env.local
```

2. Edit `.env.local` and set your OpenAI API key:
```bash
OPENAI_API_KEY=your-actual-api-key-here
```

3. Start the services:
```bash
docker compose --env-file .env.local -f docker-compose.local.yml up
```

4. Access the services:
   - Neo4j Browser: http://localhost:7474
   - MCP Neo4j Server: http://localhost:8090
   - Graphiti MCP Server: http://localhost:8091

5. Add MCP servers to Claude Desktop:
```bash
claude mcp add neo4j-cypher --transport sse http://localhost:8090/sse
claude mcp add graphiti-memory --transport sse http://localhost:8091/sse
```

### Option 2: Remote Neo4j Database

1. Copy the environment file sample:
```bash
cp .env.remote.sample .env.remote
```

2. Edit `.env.remote` and configure your remote Neo4j connection:
```bash
REMOTE_NEO4J_URI=bolt://your-remote-neo4j-host:7687
NEO4J_USER=your-neo4j-username
NEO4J_PASSWORD=your-neo4j-password
OPENAI_API_KEY=your-actual-api-key-here
```

3. Start the services:
```bash
docker compose --env-file .env.remote -f docker-compose.remote.yml up
```

4. Access the MCP services:
   - MCP Neo4j Server: http://localhost:8095
   - Graphiti MCP Server: http://localhost:8096

5. Add MCP servers to Claude Desktop:
```bash
claude mcp add remote-neo4j-cypher --transport sse http://localhost:8095/sse
claude mcp add remote-graphiti-memory --transport sse http://localhost:8096/sse
```

## Environment Variables

### Required
- `OPENAI_API_KEY`: Your OpenAI API key for the Graphiti service

### For Local Setup (docker-compose.local.yml)
- `NEO4J_USER`: Neo4j username (default: neo4j)
- `NEO4J_PASSWORD`: Neo4j password (default: demodemo)
- `NEO4J_URI`: Neo4j connection URI (default: bolt://neo4j:7687)
- `NEO4J_HTTP_PORT`: Neo4j HTTP port (default: 7474)
- `NEO4J_BOLT_PORT`: Neo4j Bolt port (default: 7687)
- `MCP_NEO4J_PORT`: MCP Neo4j server port (default: 8090)
- `GRAPHITI_MCP_PORT`: Graphiti MCP server port (default: 8091)
- `MODEL_NAME`: OpenAI model to use (default: gpt-4o-mini)
- `SEMAPHORE_LIMIT`: Concurrency limit (default: 10)

### For Remote Setup (docker-compose.remote.yml)
- `REMOTE_NEO4J_URI`: Remote Neo4j connection URI (required)
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `REMOTE_MCP_NEO4J_PORT`: MCP Neo4j server port (default: 8095)
- `REMOTE_GRAPHITI_MCP_PORT`: Graphiti MCP server port (default: 8096)
- `MODEL_NAME`: OpenAI model to use
- `SEMAPHORE_LIMIT`: Concurrency limit (default: 10)

## Stopping the Services

For local setup:
```bash
docker compose --env-file .env.local -f docker-compose.local.yml down
```

For remote setup:
```bash
docker compose --env-file .env.remote -f docker-compose.remote.yml down
```

To remove volumes as well (local setup only):
```bash
docker compose --env-file .env.local -f docker-compose.local.yml down -v
```

## Running Both Configurations

To run both local and remote configurations simultaneously:

```bash
# Using the convenience script
./start-both.sh

# Or manually
docker compose --env-file .env.local -f docker-compose.local.yml up -d
docker compose --env-file .env.remote -f docker-compose.remote.yml up -d
```

To stop both configurations:
```bash
# Using the convenience script
./stop-both.sh

# Or manually
docker compose --env-file .env.local -f docker-compose.local.yml down
docker compose --env-file .env.remote -f docker-compose.remote.yml down
```

This will start:
- Local Neo4j database on ports 7474/7687
- Local MCP servers on ports 8090/8091
- Remote MCP servers on ports 8095/8096

## Viewing Logs

```bash
# All local services
docker compose --env-file .env.local -f docker-compose.local.yml logs -f

# Specific local service
docker compose --env-file .env.local -f docker-compose.local.yml logs -f neo4j

# All remote services
docker compose --env-file .env.remote -f docker-compose.remote.yml logs -f

# Specific remote service
docker compose --env-file .env.remote -f docker-compose.remote.yml logs -f remote-graphiti-mcp
```

## MCP Configuration

The MCP servers are configured to work with Claude Desktop. To add them to your Claude configuration:

1. Open Claude Desktop settings
2. Navigate to Developer settings
3. Add the following MCP server configurations:

```json
{
  "mcpServers": {
    "neo4j-cypher": {
      "transport": "http",
      "url": "http://localhost:8090/sse"
    },
    "graphiti": {
      "transport": "http",
      "url": "http://localhost:8091/sse"
    }
  }
}
```

## Troubleshooting

### Port conflicts
If you encounter port conflicts, you can change the ports in `.env.local`:
```bash
NEO4J_HTTP_PORT=7475
NEO4J_BOLT_PORT=7688
MCP_NEO4J_PORT=8092
GRAPHITI_MCP_PORT=8093
```

### Neo4j connection issues
Ensure the Neo4j service is fully started before accessing MCP services. You can check the logs:
```bash
docker compose -f docker-compose.local.yml logs neo4j
```

### MCP server issues
Check the logs for specific MCP servers:
```bash
docker compose -f docker-compose.local.yml logs graphiti-mcp
docker compose -f docker-compose.local.yml logs mcp-neo4j-cypher-server
```