"""
Infrastructure Layer - SQLAlchemy ORM Models

Database models (tables).
"""

from sqlalchemy import Column, String, DateTime, Boolean, DECIMAL, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.infrastructure.db.database import Base


class UserModel(Base):
    """User table."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=True)
    google_id = Column(String(255), nullable=True, unique=True)
    auth_provider = Column(String(50), nullable=False, default="email")
    business_type = Column(String(100), nullable=True)  # Yangi ustun
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    transactions = relationship("TransactionModel", back_populates="user", cascade="all, delete-orphan")


class TransactionModel(Base):
    """Transaction table."""
    
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    is_expense = Column(Boolean, default=True, nullable=False)
    is_fixed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="transactions")
