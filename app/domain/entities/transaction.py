"""
Domain Layer - Transaction Entity

Moliyaviy operatsiyalar modeli.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Transaction:
    """Transaction domain entity."""
    
    id: UUID
    user_id: UUID
    date: datetime
    amount: Decimal
    description: str
    category: Optional[str] = None
    is_expense: bool = True  # True = xarajat, False = daromad
    is_fixed: bool = False  # Fixed yoki variable xarajat
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    @staticmethod
    def create_new(
        user_id: UUID,
        date: datetime,
        amount: Decimal,
        description: str,
        category: Optional[str] = None,
        is_expense: bool = True,
        is_fixed: bool = False
    ) -> 'Transaction':
        """Yangi tranzaksiya yaratish."""
        return Transaction(
            id=uuid4(),
            user_id=user_id,
            date=date,
            amount=amount,
            description=description,
            category=category,
            is_expense=is_expense,
            is_fixed=is_fixed,
            created_at=datetime.utcnow()
        )
    
    def get_signed_amount(self) -> Decimal:
        """Daromad uchun musbat, xarajat uchun manfiy qiymat qaytarish."""
        return -self.amount if self.is_expense else self.amount
