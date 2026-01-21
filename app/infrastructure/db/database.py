"""
Infrastructure Layer - Database Configuration

PostgreSQL ulanish konfiguratsiyasi.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    database_url: str = "postgresql://postgres:postgres@localhost:5432/lqxai"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"
    frontend_url: str = "http://localhost:3000"
    
    
    # OpenAI
    openai_api_key: str = ""
    
    # Local LLM (deprecated but kept for compatibility if needed elsewhere)
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b"
    
    class Config:
        env_file = ".env"


settings = Settings()

# Database engine
engine = create_engine(settings.database_url)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
