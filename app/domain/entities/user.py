"""
Domain Layer - User Entity

Foydalanuvchi modeli (clean architecture uchun).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    """User domain entity."""
    
    id: UUID
    email: str
    password_hash: Optional[str]
    google_id: Optional[str]
    auth_provider: str  # "email" yoki "google"
    business_type: Optional[str] = None  # Yangi maydon
    created_at: datetime
    
    @staticmethod
    def create_new(
        email: str,
        password_hash: Optional[str] = None,
        google_id: Optional[str] = None,
        auth_provider: str = "email",
        business_type: Optional[str] = None
    ) -> 'User':
        """Yangi foydalanuvchi yaratish."""
        return User(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            google_id=google_id,
            auth_provider=auth_provider,
            business_type=business_type,
            created_at=datetime.utcnow()
        )
    
    def verify_provider(self) -> bool:
        """Provider to'g'riligini tekshirish."""
        if self.auth_provider == "email" and not self.password_hash:
            return False
        if self.auth_provider == "google" and not self.google_id:
            return False
        return True
