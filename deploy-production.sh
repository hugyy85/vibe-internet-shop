#!/bin/bash

# Production deployment script for elena-jewelry.hugyy.ru
# This script should be run on the production server

set -e

echo "🚀 Starting production deployment of Elena Jewelry Store..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Production domain
DOMAIN="elena-jewelry.hugyy.ru"

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}Warning: Running as root. Consider using a non-root user.${NC}"
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from example...${NC}"
    cp env.example .env
    echo -e "${RED}Please edit .env file with your production settings:${NC}"
    echo "- Set a strong SECRET_KEY"
    echo "- Configure domain: $DOMAIN"
    echo "- Set DEBUG=False"
    read -p "Press enter to continue after editing .env file..."
fi

# Check if required files exist
required_files=("Dockerfile" "docker-compose.prod.yml" "nginx-site.conf" "gunicorn.conf.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Required file $file not found!${NC}"
        exit 1
    fi
done

# Configure nginx site
echo "📝 Configuring nginx site for main server..."
NGINX_SITE_CONFIG="/etc/nginx/sites-available/elena-jewelry"
if [ -f "$NGINX_SITE_CONFIG" ]; then
    echo "Nginx configuration already exists, backing up..."
    sudo cp "$NGINX_SITE_CONFIG" "$NGINX_SITE_CONFIG.bak.$(date +%Y%m%d_%H%M%S)"
fi

echo "Installing nginx site configuration..."
sudo cp nginx-site.conf "$NGINX_SITE_CONFIG"

# Enable the site
echo "Enabling nginx site..."
sudo ln -sf "$NGINX_SITE_CONFIG" /etc/nginx/sites-enabled/elena-jewelry

# Test nginx configuration
echo "Testing nginx configuration..."
if sudo nginx -t; then
    echo "✅ Nginx configuration is valid"
    echo "🔄 Reloading nginx..."
    sudo systemctl reload nginx
else
    echo "❌ Nginx configuration error!"
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true

# Clean up old images
echo "🧹 Cleaning up old Docker images..."
docker system prune -f

# Build and start containers
echo "🏗️  Building and starting containers for production..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Check if containers are running
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Production deployment successful!${NC}"
    echo -e "${BLUE}🌐 Application is available at:${NC}"
    echo "   http://$DOMAIN"
    echo "   https://$DOMAIN (when SSL is configured)"
    echo ""
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "1. Configure SSL certificate for HTTPS (use certbot)"
    echo "2. Set up domain DNS to point to this server"
    echo "3. Configure firewall (port 8000 should only be accessible locally)"
    echo "4. Set up backup schedule"
    echo "5. Monitor nginx and application logs"
    echo ""
    echo "📊 Check status: docker-compose -f docker-compose.prod.yml ps"
    echo "📝 View logs: docker-compose -f docker-compose.prod.yml logs -f"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo "📝 Check logs: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi

echo "🎉 Elena Jewelry Store deployed successfully!"