
# Serverga Deploy Qilish Bo'yicha Qo'llanma

Loyihangiz GitHub'ga muvaffaqiyatli yuklandi. Endi serverda uni ishga tushirish uchun quyidagi qadamlarni bajaring.

### 1. Serverga Kirish (SSH)
Terminal orqali serveringizga kiring:
```bash
ssh root@SERVER_IP_ADDRESS
```
*(Server IP manzilini va parolni o'zingiz bilasiz)*

### 2. Loyihani Klonlash
Agar avval klonlamagan bo'lsangiz:
```bash
git clone https://github.com/EldorKenjabayev/lQX_AI.git
cd lQX_AI
```

Agar avval bor bo'lsa, yangilang:
```bash
cd lQX_AI
git pull origin main
```

### 3. Environment Faylini Yaratish
Git'da `.env` fayli yo'q (xavfsizlik uchun). Uni serverda qo'lda yaratish kerak:
```bash
nano .env
```
Quyidagi tarkibni nusxalab, `nano` ichiga qo'ying (o'zingizning haqiqiy kalitlaringiz bilan):
```ini
DATABASE_URL=postgresql://postgres:postgrespassword@db:5432/lqxai_prod
SECRET_KEY=kuchli_maxfiy_kalit_yozing
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GOOGLE_CLIENT_ID=sizning_google_client_id
GOOGLE_CLIENT_SECRET=sizning_google_secret
GOOGLE_REDIRECT_URI=https://lqx.centraliatours.com/auth/google/callback
FRONTEND_URL=https://lqx.bublsoft.uz

OPENAI_API_KEY=sizning_openai_kalitingiz
```
*Saqlash uchun: `Ctrl+O`, `Enter`, `Ctrl+X`*

### 4. Deploy Qilish
Biz tayyorlagan `deploy.sh` skripti hammasini bajaradi (Docker build, Nginx start):
```bash
chmod +x deploy.sh
./deploy.sh
```

### 5. Tekshirish
Brauzerda kirib ko'ring:
- **Swagger UI**: [https://lqx.centraliatours.com/docs](https://lqx.centraliatours.com/docs)
- **API Test**: [https://lqx.centraliatours.com/auth/google](https://lqx.centraliatours.com/auth/google)

---
### Muammolar chiqsa:
Loglarni ko'rish:
```bash
docker-compose logs -f backend
```
Nginx loglari:
```bash
docker-compose logs -f nginx
```
