#!/bin/bash

# Stop both local and remote configurations

echo "Stopping both local and remote configurations..."

# Stop local configuration
echo "Stopping local configuration..."
docker compose -f docker-compose.local.yml down

# Stop remote configuration  
echo "Stopping remote configuration..."
docker compose -f docker-compose.remote.yml down

echo ""
echo "All services have been stopped."
echo ""
echo "To remove volumes as well, run:"
echo "  docker compose -f docker-compose.local.yml down -v"