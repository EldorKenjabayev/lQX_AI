
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.db.database import get_db
from app.infrastructure.db.models import UserModel, TransactionModel
from app.infrastructure.auth.security import get_current_user
from app.interfaces.schemas.schemas import LiquidityAnalysisRequest, LiquidityAnalysisResponse, DashboardRequest, DashboardResponse
from app.use_cases.liquidity_analysis import liquidity_analysis_use_case

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post(
    "/liquidity", 
    response_model=LiquidityAnalysisResponse,
    summary="Likvidlikni tahlil qilish va Cash Gap aniqlash",
    description="Kelajakdagi pul oqimlarini prognoz qilib, kassa uzilishlarini (cash gaps) va xavflarni aniqlaydi.",
    responses={
        200: {"description": "Tahlil muvaffaqiyatli yakunlandi"},
        400: {"description": "Analiz uchun tranzaksiyalar yetarli emas"},
        500: {"description": "Prognoz jarayonida xatolik"}
    }
)
async def analyze_liquidity(
    request: LiquidityAnalysisRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Likvidlikni chuqur tahlil qilish endpointi.
    """
    
    # Userning tranzaksiyalarini olish
    transactions_orm = db.query(TransactionModel).filter(TransactionModel.user_id == current_user.id).all()
    
    if not transactions_orm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Analiz uchun tranzaksiyalar mavjud emas"
        )
    
    # ORM -> Dict conversion
    transactions = []
    for t in transactions_orm:
        transactions.append({
            "date": t.date.strftime('%Y-%m-%d'),
            "amount": float(t.amount),
            "description": t.description,
            "category": t.category,
            "is_expense": t.is_expense,
            "is_fixed": t.is_fixed
        })
        
    result = await liquidity_analysis_use_case.run(
        user_id=current_user.id,
        transactions=transactions,
        initial_balance=request.initial_balance,
        period_days=request.period_days,
        business_type=current_user.business_type
    )
    
    
    if not result.get('success'):
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get('error', 'Analiz xatosi')
        )
        
    return LiquidityAnalysisResponse(**result)


@router.post(
    "/dashboard", 
    response_model=DashboardResponse,
    summary="Dashboard ma'lumotlarini olish",
    description="Tanlangan vaqt oralig'i (filter_type) bo'yicha daromad, xarajat va tahliliy ma'lumotlarni qaytaradi.",
    responses={
        200: {"description": "Dashboard ma'lumotlari muvaffaqiyatli olindi"},
        422: {"description": "Noto'g'ri filter turi yoki sana formati"}
    }
)
async def get_dashboard(
    request: DashboardRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dashboard analitikasi.
    """
    from app.domain.services.analytics_service import analytics_service
    
    # Userning tranzaksiyalarini olish
    transactions_orm = db.query(TransactionModel).filter(TransactionModel.user_id == current_user.id).all()
    
    # ORM -> Dict conversion
    transactions = []
    for t in transactions_orm:
        transactions.append({
            "date": t.date.strftime('%Y-%m-%d'),
            "amount": float(t.amount),
            "description": t.description,
            "category": t.category,
            "is_expense": t.is_expense,
            "is_fixed": t.is_fixed
        })
        
    data = analytics_service.get_dashboard_data(
        transactions, 
        request.filter_type, 
        request.start_date, 
        request.end_date
    )
    
    return DashboardResponse(
        success=True,
        data=data
    )

