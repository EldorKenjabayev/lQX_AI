"""
Use Case - Run Forecast

Prognoz va risk hisoblash.
"""

from typing import List, Dict, Any, Optional
from uuid import UUID
import pandas as pd

from app.domain.services.forecasting_service import forecasting_service
from app.infrastructure.llm.local_llm_client import llm_client


class RunForecastUseCase:
    """Prognoz use case."""
    
    def calculate_risk(self, forecast_data: List[Dict[str, Any]]) -> str:
        """
        Risk darajasini hisoblash.
        
        Args:
            forecast_data: Prognoz ma'lumotlari
            
        Returns:
            Risk darajasi (LOW/MEDIUM/HIGH)
        """
        if not forecast_data:
            return "UNKNOWN"
        
        # Manfiy balanslar sonini sanash
        negative_count = sum(1 for item in forecast_data if item['predicted_balance'] < 0)
        
        # Trendni tekshirish
        balances = [item['predicted_balance'] for item in forecast_data]
        is_declining = all(balances[i] >= balances[i+1] for i in range(len(balances)-1))
        
        # Risk hisoblash
        if negative_count > 0:
            return "HIGH"
        elif is_declining and balances[-1] < balances[0] * 0.5:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def run(
        self,
        user_id: UUID,
        transactions: List[Dict[str, Any]],
        initial_balance: float = 0,
        forecast_days: int = 90,
        business_type: Optional[str] = None  # Yangi argument
    ) -> Dict[str, Any]:
        """
        Prognozni ishga tushirish.
        
        Args:
            user_id: Foydalanuvchi ID
            transactions: Tranzaksiyalar
            initial_balance: Boshlang'ich balans
            forecast_days: Prognoz davomiyligi (kunlar)
            
        Returns:
            Prognoz natijalari
        """
        # Prognoz
        forecast_result = forecasting_service.run_forecast(
            transactions=transactions,
            initial_balance=initial_balance,
            forecast_days=forecast_days
        )
        
        if not forecast_result.get('success'):
            return forecast_result
        
        forecast_data_list = forecast_result['forecast']
        
        # DataFrame ni qayta tiklash (servis metodlari uchun)
        if forecast_data_list:
            forecast_df = pd.DataFrame(forecast_data_list)
        else:
            forecast_df = pd.DataFrame()

        # 1. Cash Gaps Analysis
        cash_gaps = forecasting_service.detect_cash_gaps(forecast_df)
        
        # 2. Stress Test (Historical data kerak, lekin bizda faqat forecast_df bor degani emas, 
        # bizda transactions bor. Transactions dan historical DF yasamiz)
        # Transactions dan historical daily balance yasash logikasi forecasting_service da bor (_prepare_dataframe).
        # Lekin u internal method.
        # Keling, UseCase da transactions dan yana df yasaymiz (yoki service ga public method qo'shamiz).
        # Service da _prepare_dataframe ni public qilsam yaxshi bo'ladi.
        # Hozircha tezroq yo'li: forecast_with_simulation logikasiga o'xshash, run_stress_test 
        # aslida history df ni so'raydi.
        
        # History DF ni yasash (Stress test uchun)
        # Transactions -> Daily Balance DF
        raw_df = forecasting_service.prepare_data(transactions)
        history_df = forecasting_service.calculate_daily_balance(raw_df, initial_balance)
        
        stress_test_result = forecasting_service.run_stress_test(history_df, forecast_days)
        
        # Risk hisoblash
        risk_level = self.calculate_risk(forecast_data_list)
        
        # Agar cash gap bo'lsa, risk har doim HIGH
        if cash_gaps:
            risk_level = "HIGH"
        
        # LLM orqali tavsiya (biznes konteksti + early warning bilan)
        recommendation = await llm_client.generate_recommendation(
            forecast_data={
                'current_balance': forecast_result.get('current_balance'),
                'predicted_balance_30d': forecast_data_list[29]['predicted_balance'] if len(forecast_data_list) > 29 else None,
                'method': forecast_result['metadata']['method']
            },
            risk_level=risk_level,
            business_type=business_type,
            cash_gaps=cash_gaps,
            stress_test=stress_test_result
        )
        
        result = {
            'success': True,
            'forecast': forecast_data_list,
            'risk_level': risk_level,
            'cash_gaps': cash_gaps,
            'stress_test': stress_test_result,
            'recommendation': recommendation,
            'metadata': forecast_result['metadata']
        }
        print(f"DEBUG USE CASE RETURN KEYS: {result.keys()}")
        return result


# Global instance
run_forecast_use_case = RunForecastUseCase()
