#!/bin/bash

# Production deployment script for Jewelry Store
# Make sure Docker and Docker Compose are installed

set -e

echo "🚀 Starting deployment of Jewelry Store..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from example...${NC}"
    cp env.example .env
    echo -e "${RED}Please edit .env file with your production settings before running again!${NC}"
    exit 1
fi

# Check if required files exist
required_files=("Dockerfile" "docker-compose.yml" "nginx.conf" "gunicorn.conf.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Required file $file not found!${NC}"
        exit 1
    fi
done

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans

# Build and start containers
echo "🏗️  Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo "🌐 Application is available at: http://localhost"
    echo "📊 Check status with: docker-compose ps"
    echo "📝 View logs with: docker-compose logs -f"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo "📝 Check logs with: docker-compose logs"
    exit 1
fi

echo "🎉 Deployment completed!"