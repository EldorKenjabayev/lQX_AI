# LQX AI - Liquidity Index MVP

## Tavsif
LQX AI - kichik va o'rta biznes (KO'B) uchun AI-asosida likvidlik prognoz tizimi. Bu MVP T-1 Hackathon uchun yaratilgan.

## Texnologiyalar
- **Backend**: Python 3.11, FastAPI
- **Database**: PostgreSQL
- **AI**: Local LLM (Ollama - Qwen 2.5 3B)
- **Data Science**: Pandas, NumPy, Prophet
- **Auth**: JWT, bcrypt

## Arxitektura
Clean Architecture asosida:
- `domain/` - biznes logikasi
- `use_cases/` - application logikasi
- `infrastructure/` - database, LLM
- `interfaces/` - API endpoints

## O'rnatish

### 1. Virtual muhit yaratish
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. PostgreSQL sozlash
```bash
# PostgreSQL'ni o'rnating (agar yo'q bo'lsa)
brew install postgresql@14  # macOS

# Database yaratish
createdb lqxai
```

### 4. Environment variables
```bash
cp .env.example .env
# .env faylni tahrirlang (database URL va boshqalar)
```

### 5. Ollama o'rnatish (Local LLM)
```bash
# https://ollama.ai dan yuklab oling
# Keyin:
ollama pull qwen2.5:3b
ollama serve
```

## Ishga tushirish

```bash
uvicorn app.main:app --reload
```

Server `http://localhost:8000` da ishga tushadi.

API dokumentatsiya: `http://localhost:8000/docs`

## API Endpointlar

### Auth
- `POST /auth/register` - Ro'yxatdan o'tish
- `POST /auth/login` - Tizimga kirish
- `GET /auth/google` - Google OAuth bilan tizimga kirish
- `GET /auth/google/callback` - Google OAuth callback

### Data
- `POST /data/upload/text` - Oddiy matn orqali yuklash
- `POST /data/upload/csv` - CSV fayl yuklash
- `GET /data/transactions` - Tranzaksiyalarni olish

### Forecast
- `POST /forecast/run` - Prognoz ishga tushirish

## Misol

### 1. Ro'yxatdan o'tish
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "123456"}'
```

### 2. CSV yuklash
```bash
curl -X POST http://localhost:8000/data/upload/csv \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@oquv_markazi_2_yillik_XATOLI_data.csv"
```

### 3. Prognoz
```bash
curl -X POST http://localhost:8000/forecast/run \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"initial_balance": 0, "forecast_days": 90}'
```

## Muhim
- Bu MVP tizim, production uchun emas
- Prognoz 100% aniq emas
- Buxgalteriya o'rnini bosmaydi
- Qarorlarni inson qabul qiladi

## Muallif
Eldor Kenjebayev - T-1 Hackathon
