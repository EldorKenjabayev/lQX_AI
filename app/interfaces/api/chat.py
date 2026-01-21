
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.db.database import get_db
from app.infrastructure.auth.security import get_current_user
from app.infrastructure.db.models import UserModel, TransactionModel
from app.interfaces.schemas.schemas import ChatRequest, ChatResponse
from app.use_cases.chat_advisor import chat_advisor_use_case

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
async def ask_advisor(
    request: ChatRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Moliyaviy maslahatchi bilan suhbat.
    """
    # Userning tranzaksiyalarini olish
    transactions_orm = db.query(TransactionModel).filter(TransactionModel.user_id == current_user.id).all()
    
    # ORM -> Dict conversion
    transactions = []
    for t in transactions_orm:
        transactions.append({
            "date": t.date,
            "amount": float(t.amount),
            "description": t.description,
            "category": t.category,
            "is_expense": t.is_expense
        })
        
    result = await chat_advisor_use_case.run(
        user_id=current_user.id,
        message=request.message,
        transactions=transactions,
        initial_balance=request.initial_balance
    )
    
    return ChatResponse(
        response=result['response'],
        context=result.get('context_used')
    )
