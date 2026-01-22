"""
API Endpoints - FastAPI routers

Barcha API endpointlari.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.infrastructure.db.database import get_db, settings
from app.infrastructure.db.models import UserModel, TransactionModel
from app.infrastructure.auth.security import hash_password, verify_password, create_access_token, decode_access_token
from app.interfaces.schemas.schemas import (
    UserRegisterRequest, UserLoginRequest, TokenResponse,
    UserUpdateRequest, UserResponse,
    TextUploadRequest, UploadResponse,
    ForecastRequest, ForecastResponse,
    TransactionResponse
)
from app.use_cases.upload_data import upload_data_use_case
from app.use_cases.run_forecast import run_forecast_use_case


# Routers
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
data_router = APIRouter(prefix="/data", tags=["Data"])
forecast_router = APIRouter(prefix="/forecast", tags=["Forecast"])

# Security
security = HTTPBearer()


# ==================== Auth Dependency ====================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserModel:
    """Joriy foydalanuvchini olish."""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token noto'g'ri yoki muddati tugagan"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ma'lumotlari noto'liq"
        )
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi"
        )
    
    return user


# ==================== Auth Endpoints ====================

@auth_router.post("/register", response_model=TokenResponse)
async def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """Foydalanuvchi ro'yxatdan o'tish."""
    
    # Email mavjudligini tekshirish
    existing_user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon ro'yxatdan o'tgan"
        )
    
    # Yangi foydalanuvchi
    new_user = UserModel(
        email=request.email,
        password_hash=hash_password(request.password),
        auth_provider="email",
        business_type=request.business_type
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Token yaratish
    access_token = create_access_token(data={"user_id": str(new_user.id)})
    
    return TokenResponse(
        access_token=access_token,
        user_id=str(new_user.id)
    )


@auth_router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Foydalanuvchi tizimga kirish."""
    
    # Foydalanuvchini topish
    user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri"
        )
    
    # Parolni tekshirish
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri"
        )
    
    # Token yaratish
    access_token = create_access_token(data={"user_id": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        user_id=str(user.id)
    )


@auth_router.get("/google")
async def google_login():
    """Google OAuth orqali tizimga kirish boshlash."""
    try:
        from app.infrastructure.auth.google_oauth import google_oauth_client
        from app.infrastructure.db.database import settings
        
        if not settings.google_client_id or not settings.google_client_secret:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google Google Client ID yoki Secret .env faylida sozlanmagan"
            )

        authorization_url = google_oauth_client.get_authorization_url()
        
        return {
            "authorization_url": authorization_url,
            "message": "Ushbu URL'ga o'ting va Google orqali tizimga kiring"
        }
    except Exception as e:
        print(f"Google Auth Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Google Login Xatosi: {str(e)}"
        )


@auth_router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """Google OAuth callback - token olish va foydalanuvchi yaratish/tizimga kiritish."""
    from app.infrastructure.auth.google_oauth import google_oauth_client
    
    # Code'ni token'ga almashtirish
    token_data = await google_oauth_client.exchange_code_for_token(code)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google authentication xatosi"
        )
    
    # Foydalanuvchi ma'lumotlarini olish
    user_info = await google_oauth_client.get_user_info(token_data.get("access_token"))
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google'dan foydalanuvchi ma'lumotlarini olishda xato"
        )
    
    google_id = user_info.get("id")
    email = user_info.get("email")
    
    if not google_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google ma'lumotlari to'liq emas"
        )
    
    # Foydalanuvchini topish yoki yaratish
    user = db.query(UserModel).filter(UserModel.google_id == google_id).first()
    
    if not user:
        # Yangi foydalanuvchi yaratish
        user = UserModel(
            email=email,
            google_id=google_id,
            auth_provider="google"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # JWT token yaratish
    access_token = create_access_token(data={"user_id": str(user.id)})
    
    # Frontendga redirect qilish
    frontend_url = settings.frontend_url
    redirect_url = f"{frontend_url}/auth/callback?access_token={access_token}&user_id={user.id}"
    
    return RedirectResponse(url=redirect_url)


@auth_router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """Joriy foydalanuvchi ma'lumotlarini olish."""
    return current_user


@auth_router.patch("/me", response_model=UserResponse)
async def update_user_me(
    request: UserUpdateRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Joriy foydalanuvchi ma'lumotlarini yangilash (masalan, business_type)."""
    if request.business_type:
        current_user.business_type = request.business_type
        db.commit()
        db.refresh(current_user)
    
    return current_user


# ==================== Data Endpoints ====================

@data_router.post(
    "/upload/text", 
    response_model=UploadResponse,
    summary="Matn orqali tranzaksiya yuklash",
    description="Foydalanuvchi kiritgan erkin matndan (masalan: 'Bugun 50000 so'm tushlik qildim') tranzaksiyalarni aniqlaydi.",
    responses={
        200: {"description": "Muvaffaqiyatli tahlil qilindi"},
        400: {"description": "Matnda tranzaksiya topilmadi yoki noto'g'ri format"},
        500: {"description": "Server xatosi"}
    }
)
async def upload_text(
    request: TextUploadRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Oddiy matn orqali tranzaksiya yuklash."""
    
    # Matnni parse qilish (LLM orqali)
    try:
        transactions = await upload_data_use_case.parse_text(request.text, business_type=current_user.business_type)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Matndan tranzaksiya aniqlanmadi"
        )
    
    # Ma'lumotlar bazasiga saqlash
    for txn_data in transactions:
        txn = TransactionModel(
            user_id=current_user.id,
            date=datetime.strptime(txn_data['date'], '%Y-%m-%d'),
            amount=txn_data['amount'],
            description=txn_data['description'],
            category=txn_data.get('category'),
            is_expense=txn_data.get('is_expense', True),
            is_fixed=txn_data.get('is_fixed', False)
        )
        db.add(txn)
    
    db.commit()
    
    return UploadResponse(
        success=True,
        message=f"{len(transactions)} ta tranzaksiya qo'shildi",
        transactions_count=len(transactions)
    )


@data_router.post(
    "/upload/file", 
    response_model=dict,
    summary="Fayl yuklash (Background Task)",
    description="Katta fayllarni yuklash uchun process orqa fonga o'tkaziladi va task_id qaytariladi.",
    responses={
        202: {"description": "Jarayon boshlandi"},
        400: {"description": "Fayl formati noto'g'ri"}
    }
)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Yuklanadigan fayl (max 10MB)"),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fayl yuklash va orqa fonda tahlil qilish.
    """
    from app.infrastructure.task_manager import task_manager
    from app.use_cases.upload_data import upload_data_use_case
    
    # 1. Create Task
    task_id = task_manager.create_task()
    
    # 2. Read file content into memory (UploadFile is spool file, need to read before async processing)
    # Background task faylni o'qiy olmaydi (chunki request yopiladi), shuning uchun contentni uzatamiz.
    # Lekin use_case UploadFile kutyapti. 
    # Yechim: process_upload_task metodini usecase'da emas, shu yerda yozib, usecase'ni to'g'irlash.
    # Yoki faylni vaqtincha saqlash. Memory'da saqlash (BytesIO) eng osoni.
    
    content = await file.read()
    filename = file.filename
    
    
    # Background Task function
    async def process_upload(t_id: str, f_content: bytes, f_name: str, u_id: UUID, db_local: Session, biz_type: str = None):
        try:
             # Virtual UploadFile for compatibility
            from starlette.datastructures import UploadFile as StarletteUploadFile
            from io import BytesIO
            
            # Recreate UploadFile like object
            file_obj = StarletteUploadFile(filename=f_name, file=BytesIO(f_content))
            
            from app.domain.services.file_parsing_service import file_parsing_service
            
            # Parse (with business_type)
            task_manager.update_task(t_id, status="processing", progress=5, message=f"Fayl tahlil qilinmoqda ({biz_type or 'General'})...")
            transactions_data = await file_parsing_service.parse_file(file_obj, task_id=t_id, business_type=biz_type)
            
            # Save to DB
            task_manager.update_task(t_id, progress=90, message="Ma'lumotlar saqlanmoqda...")
            
            saved_count = 0
            for txn_data in transactions_data:
                txn = TransactionModel(
                    user_id=u_id,
                    date=datetime.strptime(txn_data['date'], '%Y-%m-%d'),
                    amount=txn_data['amount'],
                    description=txn_data['description'],
                    category=txn_data.get('category'),
                    is_expense=txn_data.get('is_expense', True),
                    is_fixed=txn_data.get('is_fixed', False)
                )
                db_local.add(txn)
                saved_count += 1
            
            db_local.commit()
            
            task_manager.update_task(
                t_id, 
                status="completed", 
                progress=100, 
                message=f"Tayyor! {saved_count} ta tranzaksiya yuklandi.",
                result={"count": saved_count}
            )
            
        except Exception as e:
            print(f"Background Task Error: {e}")
            task_manager.update_task(t_id, status="failed", error=str(e))
    
    # 3. Add to background tasks
    from app.infrastructure.db.database import SessionLocal
    def bg_wrapper(t_id, f_content, f_name, u_id, biz_type):
        # Create fresh session for background thread
        db_bg = SessionLocal()
        try:
             import asyncio
             # Async functionni sync wrapper ichida yurgizish
             loop = asyncio.new_event_loop()
             asyncio.set_event_loop(loop)
             loop.run_until_complete(process_upload(t_id, f_content, f_name, u_id, db_bg, biz_type))
             loop.close()
        finally:
            db_bg.close()

    background_tasks.add_task(bg_wrapper, task_id, content, filename, current_user.id, current_user.business_type)
    
    return {"task_id": task_id, "message": "Jarayon boshlandi"}


@data_router.get("/upload/status/{task_id}")
async def get_upload_status(task_id: str):
    """
    Background task statusini tekshirish.
    """
    from app.infrastructure.task_manager import task_manager
    
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task topilmadi")
        
    return task


@data_router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Foydalanuvchi tranzaksiyalarini olish."""
    
    transactions = db.query(TransactionModel).filter(
        TransactionModel.user_id == current_user.id
    ).order_by(TransactionModel.date.desc()).all()
    
    return transactions


# ==================== Forecast Endpoints ====================

@forecast_router.post("/run", response_model=ForecastResponse)
async def run_forecast(
    request: ForecastRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Prognoz ishga tushirish."""
    
    # Tranzaksiyalarni olish
    transactions_db = db.query(TransactionModel).filter(
        TransactionModel.user_id == current_user.id
    ).all()
    
    if not transactions_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avval tranzaksiyalar yuklanishi kerak"
        )
    
    # Tranzaksiyalarni dict formatga aylantirish
    transactions = []
    for txn in transactions_db:
        transactions.append({
            'date': txn.date.strftime('%Y-%m-%d'),
            'amount': float(txn.amount),
            'description': txn.description,
            'category': txn.category,
            'is_expense': txn.is_expense,
            'is_fixed': txn.is_fixed
        })
    
    # Prognoz
    forecast_result = await run_forecast_use_case.run(
        user_id=current_user.id,
        transactions=transactions,
        initial_balance=request.initial_balance,
        forecast_days=request.forecast_days,
        business_type=current_user.business_type  # Userdan olish
    )
    
    if not forecast_result.get('success'):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=forecast_result.get('error', 'Prognoz xatosi')
        )
    
    return ForecastResponse(**forecast_result)


# ==================== Transaction Management ====================

@data_router.delete("/transaction/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tranzaksiyani o'chirish."""
    try:
        txn_uuid = UUID(transaction_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Noto'g'ri ID formati")

    transaction = db.query(TransactionModel).filter(
        TransactionModel.id == txn_uuid,
        TransactionModel.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Tranzaksiya topilmadi")

    db.delete(transaction)
    db.commit()
    return None


@data_router.delete("/analytics/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_transactions(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Barcha tranzaksiyalarni o'chirish."""
    db.query(TransactionModel).filter(
        TransactionModel.user_id == current_user.id
    ).delete()
    db.commit()
    return None


from app.interfaces.schemas.schemas import TransactionUpdateRequest

@data_router.patch("/transaction/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    request: TransactionUpdateRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tranzaksiyani tahrirlash."""
    try:
        txn_uuid = UUID(transaction_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Noto'g'ri ID formati")

    transaction = db.query(TransactionModel).filter(
        TransactionModel.id == txn_uuid,
        TransactionModel.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Tranzaksiya topilmadi")

    # Update logic
    if request.date:
        transaction.date = datetime.strptime(request.date, '%Y-%m-%d')
    if request.amount is not None:
        transaction.amount = request.amount
    if request.description is not None:
        transaction.description = request.description
    if request.category is not None:
        transaction.category = request.category
    if request.is_expense is not None:
        transaction.is_expense = request.is_expense
    if request.is_fixed is not None:
        transaction.is_fixed = request.is_fixed

    db.commit()
    db.refresh(transaction)
    return transaction
