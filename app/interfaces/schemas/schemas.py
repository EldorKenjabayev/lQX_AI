"""
API Schemas - Pydantic models

Request va response uchun Pydantic modellari.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ==================== Auth Schemas ====================

class UserRegisterRequest(BaseModel):
    """Foydalanuvchi ro'yxatdan o'tish."""
    email: EmailStr
    password: str = Field(..., min_length=6)
    business_type: Optional[str] = Field(None, description="Biznes turi: savdo, oquv_markazi, ishlab_chiqarish")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "business_type": "savdo"
            }
        }


class UserLoginRequest(BaseModel):
    """Foydalanuvchi tizimga kirish."""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }


class UserUpdateRequest(BaseModel):
    """Foydalanuvchi ma'lumotlarini yangilash."""
    business_type: str = Field(..., description="Biznes turi: savdo, oquv_markazi, ishlab_chiqarish")

    class Config:
        json_schema_extra = {
            "example": {
                "business_type": "savdo"
            }
        }


class UserResponse(BaseModel):
    """Foydalanuvchi ma'lumotlari."""
    id: UUID
    email: EmailStr
    business_type: Optional[str] = None
    auth_provider: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "business_type": "savdo",
                "auth_provider": "google"
            }
        }


class TokenResponse(BaseModel):
    """Token javobi."""
    access_token: str
    token_type: str = "bearer"
    user_id: str


# ==================== Transaction Schemas ====================

class TransactionCreate(BaseModel):
    """Tranzaksiya yaratish."""
    date: str = Field(..., description="YYYY-MM-DD formati")
    amount: float
    description: str
    category: Optional[str] = None
    is_expense: bool = True
    is_fixed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-05-20",
                "amount": 150000,
                "description": "Ofis uchun qog'oz",
                "category": "Ofis xarajatlari",
                "is_expense": True,
                "is_fixed": False
            }
        }


class TransactionResponse(BaseModel):
    """Tranzaksiya javobi."""
    id: UUID
    user_id: UUID
    date: datetime
    amount: float
    description: str
    category: Optional[str]
    is_expense: bool
    is_fixed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Data Upload Schemas ====================

class TextUploadRequest(BaseModel):
    """Oddiy matn yuklash."""
    text: str = Field(..., description="Tranzaksiya haqida matn")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Bugun 50000 so'm taksi uchun to'ladim"
            }
        }


class UploadResponse(BaseModel):
    """Yuklash javobi."""
    success: bool
    message: str
    transactions_count: Optional[int] = None


# ==================== Forecast Schemas ====================

class ForecastRequest(BaseModel):
    """Prognoz so'rovi."""
    initial_balance: float = Field(0, description="Boshlang'ich balans")
    forecast_days: int = Field(90, ge=30, le=365, description="Prognoz davri (kun)")

    class Config:
        json_schema_extra = {
            "example": {
                "initial_balance": 10000000,
                "forecast_days": 90
            }
        }


class ForecastDataPoint(BaseModel):
    """Prognoz nuqtasi."""
    date: str
    predicted_balance: float
    lower_bound: float
    upper_bound: float


class ForecastResponse(BaseModel):
    """Prognoz javobi."""
    success: bool
    forecast: List[ForecastDataPoint]
    risk_level: str
    recommendation: str
    metadata: dict


# ==================== Chat Schemas ====================

class ChatRequest(BaseModel):
    """Chat so'rovi."""
    message: str
    initial_balance: float = 0

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Keyingi oyda qancha xarajat kutyapsiz?",
                "initial_balance": 5000000
            }
        }


class ChatResponse(BaseModel):
    """Chat javobi."""
    response: str # Original faylda bu maydon yo'q edi, lekin endpoint ishlatadi. Keling qo'shamiz yoki asl holicha qoldiramiz.


# ==================== Analytics Schemas ====================

class LiquidityAnalysisRequest(BaseModel):
    """Likvidlik analizi so'rovi."""
    period_days: int = Field(..., ge=15, le=365, description="Analiz davri (kunlarda)")
    initial_balance: float = 0

    class Config:
        json_schema_extra = {
            "example": {
                "period_days": 30,
                "initial_balance": 2000000
            }
        }


class LiquidityAnalysisResponse(BaseModel):
    """Likvidlik analizi javobi."""
    success: bool
    summary: Dict[str, Any]
    cash_gaps: List[Dict[str, Any]]
    chart_data: List[Dict[str, Any]]


class DashboardRequest(BaseModel):
    """Dashboard ma'lumotlari uchun so'rov."""
    filter_type: str = Field(..., description="Filtr turi: last_7_days, this_month, last_month, this_year, custom")
    start_date: Optional[str] = Field(None, description="Boshlanish sanasi (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="Tugash sanasi (YYYY-MM-DD)")
    category: Optional[str] = Field(None, description="Kategoriya bo'yicha filtrlash")
    min_amount: Optional[float] = Field(None, description="Minimal summa")
    max_amount: Optional[float] = Field(None, description="Maksimal summa")

    class Config:
        json_schema_extra = {
            "example": {
                "filter_type": "last_7_days",
                "category": "Oziq-ovqat"
            }
        }



class TopExpense(BaseModel):
    """Eng katta xarajatlar."""
    category: str
    amount: float
    percentage: float


class ChartPoint(BaseModel):
    """Grafik uchun ma'lumot nuqtasi."""
    date: str
    income: float
    expense: float
    net_change: float


class DashboardSummary(BaseModel):
    """Dashboard umumiy ko'rsatkichlari."""
    total_income: float
    total_expense: float
    net_profit: float = Field(0.0, description="Sof foyda (Kirim - Chiqim)")
    savings_rate: float = Field(0.0, description="Tejab qolish foizi")


class DashboardData(BaseModel):
    """Dashboard asosiy ma'lumotlari."""
    current_balance: float = Field(..., description="Joriy balans")
    growth_percentage: float = Field(..., description="O'sish foizi")
    top_expenses: List[TopExpense] = Field(default=[], description="Eng katta xarajatlar ro'yxati")
    summary: DashboardSummary = Field(..., description="Kirim va chiqimlar yig'indisi")
    charts: List[ChartPoint] = Field(default=[], description="Grafiklar uchun vaqt bo'yicha ma'lumotlar")
    details: Dict[str, Any] = Field(default={}, description="Qo'shimcha detallar")


class DashboardResponse(BaseModel):
    """Dashboard javobi."""
    success: bool
    data: DashboardData

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "current_balance": 5400000,
                    "growth_percentage": 12.5,
                    "top_expenses": [
                        {"category": "Oziq-ovqat", "amount": 1200000, "percentage": 45.0},
                        {"category": "Ijara", "amount": 500000, "percentage": 18.2}
                    ],
                    "summary": {
                        "total_income": 10000000,
                        "total_expense": 4600000
                    },
                    "charts": {},
                    "details": {}
                }
            }
        }


class FilterOptionsResponse(BaseModel):
    """Filtrlash uchun mavjud opsiyalar."""
    categories: List[str]
    min_date: Optional[str]
    max_date: Optional[str]
    min_amount: float
    max_amount: float
