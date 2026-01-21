
from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd

from app.domain.services.forecasting_service import forecasting_service
from app.infrastructure.llm.local_llm_client import llm_client

class LiquidityAnalysisUseCase:
    """
    Likvidlikni chuqur tahlil qilish use case.
    Foydalanuvchi tanlagan davr uchun prognoz va tavsiyalar beradi.
    """
    
    async def run(
        self, 
        user_id: Any, 
        transactions: List[Dict[str, Any]], 
        initial_balance: float, 
        period_days: int,
        business_type: str = None
    ) -> Dict[str, Any]:
        """
        Analizni ishga tushirish.
        """
        # 1. Forecasting Service orqali prognoz qilish
        # Kichik hack: forecast_days ni period_days ga tenglaymiz
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Prepare data (Forecast servisi ichidagi metodni chaqirishimiz mumkin, lekin u private bo'lishi mumkin)
        # Shuning uchun forecasting_service.predict_cash_flow ni ishlatamiz
        forecast_df = forecasting_service.predict_cash_flow(
            df, 
            initial_balance=initial_balance, 
            days=period_days
        )
        
        if forecast_df.empty:
            return {"success": False, "error": "Prognoz uchun ma'lumot yetarli emas"}

        # 2. Cash Gaps (Kassa uzilishlari)
        cash_gaps = forecasting_service.detect_cash_gaps(forecast_df)
        
        # 3. Minimum va Maximum balans
        min_balance = forecast_df['predicted_balance'].min()
        max_balance = forecast_df['predicted_balance'].max()
        final_balance = forecast_df['predicted_balance'].iloc[-1]
        
        liquidity_status = "Yaxshi"
        if cash_gaps:
            liquidity_status = "Xavfli (Kassa uzilishi)"
        elif min_balance < initial_balance * 0.1: # Agar balans 10% dan tushib ketsa
            liquidity_status = "O'rtacha (Past balans)"

        # 4. Tavsiyalar (LLM)
        recommendation = await llm_client.generate_recommendation(
            forecast_data={
                "min_balance": min_balance,
                "final_balance": final_balance,
                "liquidity_status": liquidity_status,
                "period_days": period_days
            },
            risk_level=liquidity_status,
            business_type=business_type,
            cash_gaps=cash_gaps
        )
        
        # 5. Summary
        summary = {
            "period_days": period_days,
            "liquidity_status": liquidity_status,
            "min_balance": min_balance,
            "final_balance": final_balance,
            "cash_gaps_count": len(cash_gaps),
            "recommendation": recommendation
        }

        return {
            "success": True,
            "summary": summary,
            "cash_gaps": cash_gaps,
            # Grafik uchun qisqartirilgan data
            "chart_data": forecast_df[['date', 'predicted_balance']].to_dict(orient='records')
        }

liquidity_analysis_use_case = LiquidityAnalysisUseCase()
