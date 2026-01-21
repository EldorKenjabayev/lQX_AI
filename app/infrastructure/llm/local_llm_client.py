"""
Infrastructure Layer - OpenAI Client

OpenAI GPT modellari bilan ishlash (Local LLM o'rniga).
"""

from openai import AsyncOpenAI
from typing import Optional, Dict, Any, List
from app.infrastructure.db.database import settings


class OpenAIClient:
    """OpenAI GPT bilan ishlash uchun client."""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        # Agar API kalit bo'lmasa, client ishlamaydi (yoki xato beradi)
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("OGOHLANTIRISH: OPENAI_API_KEY topilmadi!")

        self.model = "gpt-4-turbo-preview" # Yoki 'gpt-3.5-turbo'
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        GPT'dan javob olish.
        """
        if not self.client:
            return "OpenAI API kaliti sozlanmagan."

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI xatosi: {str(e)}")
            return ""
    
    async def parse_text_to_transactions(self, text: str) -> list[Dict[str, Any]]:
        """
        Oddiy matnni tranzaksiyalarga aylantirish (GPT orqali).
        """
        system_prompt = """Sen moliyaviy ma'lumotlarni tahlil qiluvchi AI assistantsan.
Foydalanuvchi oddiy matn ko'rinishida moliyaviy operatsiyalarni kiritadi.
Sen ularni quyidagi JSON formatga aylantiring kerak:

[
  {
    "date": "YYYY-MM-DD",
    "amount": 1000000,
    "description": "tavsif",
    "category": "kategoriya",
    "is_expense": true/false,
    "is_fixed": true/false
  }
]

- Agar sana ko'rsatilmagan bo'lsa, joriy oyni ishlat.
- Xarajat uchun is_expense=true, daromad uchun false.
- Doimiy xarajatlar (ijara, maosh) uchun is_fixed=true.
- Faqat JSON formatida javob ber, boshqa matn qo'shma.
- KATEGORIYA nomlari faqat O'ZBEK tilida bo'lsin (Masalan: "Food" -> "Oziq-ovqat", "Salary" -> "Maosh", "Rent" -> "Ijara").
"""
        from datetime import datetime
        today_str = datetime.now().strftime('%Y-%m-%d')
        prompt = f"Bugungi sana: {today_str}. Quyidagi matnni tahlil qilib, JSON formatda tranzaksiyalar ro'yxatini ber:\n\n{text}"
        
        response = await self.generate(prompt, system_prompt=system_prompt, temperature=0.3)
        
        # JSON parse qilish
        try:
            import json
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            transactions = json.loads(cleaned)
            if not isinstance(transactions, list):
                # Agar list bo'lmasa, demak format noto'g'ri
                 raise ValueError("LLM javobi kutilgan formatda emas (list).")
                 
            if not transactions:
                 # Agar bo'sh list bo'lsa
                 raise ValueError("Matnda moliyaviy tranzaksiyalar topilmadi.")

            return transactions
        except Exception as e:
            # Xatoni yuqoriga uzatish, shunda userga ko'rsata olamiz
            raise ValueError(f"Ma'lumotlarni tahlil qilib bo'lmadi: {str(e)}")
    
    async def generate_recommendation(
        self,
        forecast_data: Dict[str, Any],
        risk_level: str,
        business_type: Optional[str] = None,
        cash_gaps: List[Dict[str, Any]] = [],
        stress_test: Dict[str, Any] = {}
    ) -> str:
        """
        Prognoz va risk asosida tavsiya yaratish (Risk Manager rejimi).
        """
        context = "O'zbekiston bozori"
        biz_type_str = f"Biznes turi: {business_type}" if business_type else "Biznes turi: Noma'lum"
        
        gap_warning = ""
        if cash_gaps:
            first_gap = cash_gaps[0]
            gap_warning = f"DİQQAT: {first_gap['date']} sanasida {first_gap['deficit']:,.0f} so'm kassa uzilishi (cash gap) kutilmoqda!"
            
        stress_warning = ""
        if stress_test and not stress_test.get('is_survived', True):
            stress_warning = f"OGOHLANTIRISH: Stress test (Daromad -20%, Xarajat +10%) natijasida biznes inqirozga uchraydi. Minimal balans: {stress_test.get('min_balance'):,.0f} so'm."

        system_prompt = f"""Sen tajribali Inqiroz Menejeri (Risk Manager) va moliyaviy tahlilchisan.
Sen O'zbekiston bozorini yaxshi tushunasan. Seni vazifang - biznes egasini kutilayotgan moliyaviy xavflardan erta ogohlantirish.
Kontekst: {context}. {biz_type_str}.

Qoidalar:
1. Agar kassa uzilishi (cash gap) bo'lsa, zudlik bilan ANIQ ogohlantirish ber (sana va summa).
2. "Hammasi yaxshi bo'ladi" deb ovutmang, muammoni ro'y-rost ayting.
3. Stress test natijalariga urg'u ber.
4. Tushunarsiz bank terminlarini ishlatma, sodda va keskin gapir.
5. 2-3 ta aniq, amaliy yechim taklif qil (Masalan: "Xarajatni kesish", "Faktoring", "Qarz undirish").
"""
        
        prompt = f"""
Holat:
Risk Darajasi: {risk_level}
{gap_warning}
{stress_warning}

Prognoz qisqacha:
{forecast_data}

SHOSHILINCH TAVSIYA BER:
"""
        return await self.generate(
            prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=500
        )
    
    async def chat_with_advisor(
        self,
        user_message: str,
        context_data: Dict[str, Any]
    ) -> str:
        """
        Foydalanuvchi bilan interaktiv muloqot.
        Context data ichida: forecast, risk, anomalies, liquidity_check bo'lishi mumkin.
        """
        system_prompt = """Sen LQX AI - biznes egalari uchun aqlli moliyaviy maslahatchisan.
Sening vazifang - biznes egasiga sodda, londa va foydali maslahatlar berish.

Qoidalar:
1. Agar foydalanuvchi "Mashina olsam bo'ladimi?" yoki shunga o'xshash katta xarajat haqida so'rasa, berilgan 'liquidity_check' ma'lumotiga tayanib javob ber. O'zboshimchalik bilan "ha" yoki "yo'q" dema.
2. Agar anomaliyalar bo'lsa, ularni ko'rsatib o't (masalan: "Elektr narxi oshib ketibdi").
3. O'zbek tilida, samimiy va professional gapir.
4. Javobing qisqa bo'lsin (maksimum 3-4 jumla), lekin mazmunli.
"""
        
        # Kontekstni matnlashtirish
        context_str = "Hozirgi Biznes Holati:\n"
        
        if 'risk_level' in context_data:
            context_str += f"- Risk Darajasi: {context_data['risk_level']}\n"
            
        if 'liquidity_check' in context_data and context_data['liquidity_check']:
            check = context_data['liquidity_check']
            context_str += f"- Katta xarajat tekshiruvi: {check['message']}\n"
            
        if 'anomalies' in context_data and context_data['anomalies']:
            context_str += "- Anomaliyalar (Diqqat qiling):\n"
            for a in context_data['anomalies']:
                context_str += f"  * {a['message']}\n"
                
        if 'cash_gaps' in context_data and context_data['cash_gaps']:
             context_str += f"- Kassa uzilishi kutilmoqda! ({len(context_data['cash_gaps'])} ta holat)\n"

        prompt = f"""
{context_str}

Foydalanuvchi savoli: {user_message}

Javob:
"""
        return await self.generate(prompt, system_prompt=system_prompt, temperature=0.7)


# Global instance - nomini 'llm_client' deb qoldiramiz, shunda boshqa fayllarni o'zgartirish shart emas
llm_client = OpenAIClient()
