"""
LQX AI - Main Application

FastAPI application entrypoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.interfaces.api.endpoints import auth_router, data_router, forecast_router
from app.interfaces.api.analytics import router as analytics_router
from app.interfaces.api.chat import router as chat_router
from app.infrastructure.db.database import Base, engine


# Ma'lumotlar bazasi jadvallarini yaratish
Base.metadata.create_all(bind=engine)


# FastAPI app
app = FastAPI(
    title="LQX AI API",
    description="Liquidity Index AI - Kichik va o'rta biznes uchun likvidlik prognoz tizimi",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Production'da aniq originlarni ko'rsating
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth_router)
app.include_router(data_router)
app.include_router(forecast_router)
app.include_router(analytics_router)
app.include_router(chat_router, prefix="/chat", tags=["Chat"])


@app.get("/")
async def root():
    """Health check."""
    return {
        "message": "LQX AI API ishlamoqda",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
