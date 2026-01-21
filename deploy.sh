
#!/bin/bash

# Ranglar
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}LQX AI Deployment Script${NC}"

# 1. Pull latest changes (agar git da bo'lsa)
# git pull origin main

# Docker Compose buyrug'ini aniqlash
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# 2. Build and Run Docker Containers
echo -e "${GREEN}Docker containerlarni qurish va ishga tushirish ($DOCKER_COMPOSE)...${NC}"
$DOCKER_COMPOSE up -d --build

# 3. Status check
echo -e "${GREEN}Status:${NC}"
$DOCKER_COMPOSE ps

echo -e "${GREEN}Deployment yakunlandi!${NC}"
echo -e "API manzil: http://lqx.centraliatours.com (Agar DNS va Port Forwarding to'g'ri bo'lsa)"
echo -e "Mahalliy test: http://localhost:8001/docs"
