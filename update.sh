#!/bin/bash

# Ranglar
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== LQX AI Update Script ===${NC}"

# 1. Git Pull
echo -e "${YELLOW}1. Kod yangilanmoqda (git pull)...${NC}"
git pull origin main
if [ $? -ne 0 ]; then
    echo -e "${RED}Xatolik: Git pull amalga oshmadi. Iltimos, konfliktlarni tekshiring.${NC}"
    exit 1
fi

# 2. Docker Compose buyrug'ini aniqlash
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# 3. Build and Run Docker Containers
echo -e "${YELLOW}2. Docker containerlar yangilanmoqda va qayta ishga tushirilmoqda...${NC}"
# Eski konteynerlarni to'xtatish (xavfsizlik uchun, lekin shart emas har doim)
# $DOCKER_COMPOSE down 

# Yangilab ishga tushirish
$DOCKER_COMPOSE up -d --build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}=== Muvaffaqiyatli yakunlandi! ===${NC}"
    echo -e "Status:"
    $DOCKER_COMPOSE ps
else
    echo -e "${RED}Xatolik: Docker containerlarni ishga tushirishda muammo bo'ldi.${NC}"
    exit 1
fi
