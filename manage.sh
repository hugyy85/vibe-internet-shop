#!/bin/bash

# Management script for Jewelry Store application
# Usage: ./manage.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${BLUE}Jewelry Store Management Script${NC}"
    echo ""
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start     - Start the application"
    echo "  stop      - Stop the application"
    echo "  restart   - Restart the application"
    echo "  logs      - Show application logs"
    echo "  status    - Show container status"
    echo "  build     - Rebuild containers"
    echo "  backup    - Backup application data"
    echo "  update    - Update and restart application"
    echo "  cleanup   - Remove unused Docker resources"
    echo "  shell     - Open shell in app container"
    echo "  help      - Show this help message"
}

case "$1" in
    start)
        echo -e "${GREEN}🚀 Starting Jewelry Store...${NC}"
        docker-compose up -d
        echo -e "${GREEN}✅ Application started!${NC}"
        echo "🌐 Visit: http://localhost"
        ;;
    stop)
        echo -e "${YELLOW}🛑 Stopping Jewelry Store...${NC}"
        docker-compose down
        echo -e "${GREEN}✅ Application stopped!${NC}"
        ;;
    restart)
        echo -e "${YELLOW}🔄 Restarting Jewelry Store...${NC}"
        docker-compose restart
        echo -e "${GREEN}✅ Application restarted!${NC}"
        ;;
    logs)
        echo -e "${BLUE}📝 Showing logs (Ctrl+C to exit)...${NC}"
        docker-compose logs -f
        ;;
    status)
        echo -e "${BLUE}📊 Container Status:${NC}"
        docker-compose ps
        ;;
    build)
        echo -e "${YELLOW}🏗️  Rebuilding containers...${NC}"
        docker-compose build --no-cache
        echo -e "${GREEN}✅ Build completed!${NC}"
        ;;
    backup)
        echo -e "${BLUE}💾 Creating backup...${NC}"
        timestamp=$(date +"%Y%m%d_%H%M%S")
        mkdir -p backups
        cp -r static backups/static_$timestamp
        cp price_v2.csv backups/price_v2_$timestamp.csv
        echo -e "${GREEN}✅ Backup created in backups/ directory${NC}"
        ;;
    update)
        echo -e "${YELLOW}📦 Updating application...${NC}"
        git pull origin main
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        echo -e "${GREEN}✅ Update completed!${NC}"
        ;;
    cleanup)
        echo -e "${YELLOW}🧹 Cleaning up Docker resources...${NC}"
        docker system prune -f
        docker volume prune -f
        echo -e "${GREEN}✅ Cleanup completed!${NC}"
        ;;
    shell)
        echo -e "${BLUE}🐚 Opening shell in app container...${NC}"
        docker-compose exec app /bin/bash
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac