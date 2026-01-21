
#!/bin/bash

# Ranglar
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}LQX AI Deployment Script${NC}"

# 1. Pull latest changes (agar git da bo'lsa)
# git pull origin main

# 2. Build and Run Docker Containers
echo -e "${GREEN}Docker containerlarni qurish va ishga tushirish...${NC}"
docker-compose up -d --build

# 3. Status check
echo -e "${GREEN}Status:${NC}"
docker-compose ps

echo -e "${GREEN}Deployment yakunlandi!${NC}"
echo -e "API manzil: http://lqx.centraliatours.com (Agar DNS va Port Forwarding to'g'ri bo'lsa)"
echo -e "Mahalliy test: http://localhost:8001/docs"
