
from typing import Dict, Any, List, Optional
from uuid import UUID
import re

from app.domain.services.forecasting_service import forecasting_service
from app.infrastructure.llm.local_llm_client import llm_client

class ChatAdvisorUseCase:
    """Chat orqali maslahat berish use case."""
    
    async def run(
        self,
        user_id: UUID,
        message: str,
        transactions: List[Dict[str, Any]], # Context uchun transaction history kerak
        initial_balance: float = 0
    ) -> Dict[str, Any]:
        
        # 1. Ma'lumotlarni tayyorlash va tahlil qilish
        raw_df = forecasting_service.prepare_data(transactions)
        
        # Agar transactionlar bo'lmasa
        if raw_df.empty:
             return {
                'response': "Hali yetarli ma'lumot yo'q. Iltimos, oldin tranzaksiyalarni yuklang (CSV yoki kiritish orqali)."
            }
            
        daily_df = forecasting_service.calculate_daily_balance(raw_df, initial_balance)
        
        # Forecast qilish (30 kunlik) - kontekst uchun
        forecast_df, _ = forecasting_service.forecast_with_simulation(daily_df, forecast_days=30)
        
        # Anomaliyalarni aniqlash
        anomalies = forecasting_service.detect_anomalies(raw_df)
        
        # Cash Gaps
        cash_gaps = forecasting_service.detect_cash_gaps(forecast_df)
        
        # 2. Intent Detection (Soddalashtirilgan)
        # "Mashina", "uy", "xarajat", "sotib olsam" kabi so'zlarni va summani qidiramiz.
        liquidity_check = None
        
        # Oddiy regex: Raqam + "so'm" yoki shunchaki katta raqam va "olsam" so'zi
        # Masalan: "100 mln ga mashina olsam bo'ladimi?"
        # Regex: (\d+)\s*(mln|ming|k)?
        
        expense_intent = self._detect_expense_intent(message)
        if expense_intent:
            amount = expense_intent
            liquidity_check = forecasting_service.check_liquidity(forecast_df, amount)
            
        # 3. LLM ga kontekst bilan murojaat qilish
        context_data = {
            'risk_level': "HIGH" if cash_gaps else "LOW",
            'anomalies': anomalies,
            'cash_gaps': cash_gaps,
            'liquidity_check': liquidity_check
        }
        
        llm_response = await llm_client.chat_with_advisor(message, context_data)
        
        return {
            'response': llm_response,
            'context_used': context_data
        }
        
    def _detect_expense_intent(self, text: str) -> Optional[float]:
        """
        Matndan xarajat summasini ajratib olishga urinish.
        """
        text = text.lower()
        if "olsam" in text or "xarajat" in text or "sotib" in text:
            # Raqamlarni qidirish
            # 1. "10000" yoki "10 000"
            # 2. "10 mln", "500 ming", "2 k"
            
            # Oddiy yechim: "mln" ni ko'paytirish
            import re
            
            # Pattern: raqam (yoki float) va keyin 'mln' so'zi
            mln_match = re.search(r'(\d+(?:[.,]\d+)?)\s*mln', text)
            if mln_match:
                val = float(mln_match.group(1).replace(',', '.'))
                return val * 1000000
                
            ming_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(ming|k)', text)
            if ming_match:
                val = float(ming_match.group(1).replace(',', '.'))
                return val * 1000
                
            # Shunchaki katta raqam
            simple_match = re.search(r'(\d{4,})', text.replace(' ', ''))
            if simple_match:
                 return float(simple_match.group(1))
                 
        return None

chat_advisor_use_case = ChatAdvisorUseCase()
