"""
Infrastructure Layer - OpenAI Client

OpenAI GPT modellari bilan ishlash (Local LLM o'rniga).
"""

from openai import AsyncOpenAI
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from app.infrastructure.db.database import settings


class OpenAIClient:
    """OpenAI GPT bilan ishlash uchun client."""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        
        # Ollama Configuration
        self.use_local = False
        import os
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

        if self.api_key and "sk-" in self.api_key:
             # Use OpenAI
             self.client = AsyncOpenAI(api_key=self.api_key)
             self.model = "gpt-4-turbo-preview"
        else:
             # Fallback to Ollama (Local LLM)
             print(f"INFO: OpenAI key topilmadi. Ollama ({ollama_host}) ishlatilmoqda.")
             self.use_local = True
             self.client = AsyncOpenAI(
                 base_url=f"{ollama_host}/v1",
                 api_key="ollama" # required but ignored
             )
             self.model = ollama_model
    
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
    
    async def parse_text_to_transactions(self, text: str, business_type: Optional[str] = None) -> list[Dict[str, Any]]:
        """
        Oddiy matnni tranzaksiyalarga aylantirish (GPT orqali).
        business_type: 'savdo', 'oquv_markazi', 'ishlab_chiqarish'
        """
        
        # Biznes turiga qarab maxsus prompt va mantiqiy zanjir (CoT)
        biz_context = "Umumiy moliya"
        biz_rules = ""
        
        if business_type == "oquv_markazi":
            biz_context = "O'quv Markazi (Ta'lim)"
            biz_rules = """
- KONTEKSTNI TAHLIL QIL:
  - Agar "bola", "o'quvchi", "guruh" so'zlari qatnashsa va pul kirimi bo'lsa -> "O'quv kursi to'lovi" (Daromad).
  - Agar "o'qituvchi", "domla", "usta" so'zlari qatnashsa va pul chiqimi bo'lsa -> "O'qituvchi maoshi" (Xarajat).
  - "Parta", "Doska", "Proyektor", "Kompyuter" -> "Jihozlar" (Xarajat).
  - "Reklama", "Target", "Flayer", "SMM" -> "Marketing" (Xarajat).
  - "Arenda", "Joy puli" -> "Ijara" (Xarajat, Doimiy).
  - "Svet", "Gaz", "Suv", "Internet" -> "Kommunal" (Xarajat).
  - "Soliq", "Patent" -> "Soliqlar" (Xarajat).
  - Muhim: "Xarajat" yoki "Chiqim" deb umumiy nomlama! Aniq turini yoz.
"""
        elif business_type == "savdo":
             biz_context = "Savdo va Do'kon (Retail)"
             biz_rules = """
- KONTEKSTNI TAHLIL QIL:
  - "Savdo", "Kassa", "Terminal", "Naqd" (agar kirim bo'lsa) -> "Savdo tushumi" (Daromad).
  - "Tovar", "Yuk", "Kargo", "Optom" -> "Tovar xaridi" (Xarajat).
  - "Vozvrat", "Qaytdi" -> "Tovar qaytishi" (Xarajat).
  - "Arenda", "Svet", "Soliq" -> "Operatsion xarajatlar" (Xarajat).
  - "Inkassatsiya" -> "Inkassatsiya" (Xarajat transfer).
  - Muhim: "Xarajat" deb yozma, masalan "Do'kon ijarasi", "Transport" deb aniq yoz.
"""
        elif business_type == "ishlab_chiqarish":
             biz_context = "Ishlab Chiqarish (Zavod/Sex)"
             biz_rules = """
- KONTEKSTNI TAHLIL QIL:
  - "Xom-ashyo", "Material", "Metal", "Mato", "Ip" -> "Xom-ashyo xaridi" (Xarajat).
  - "Usta haq", "Ishchi puli", "Tikuvchi" -> "Ish haqi" (Xarajat).
  - "Sotildi", "Partiya ketdi", "Mijoz to'ladi" -> "Mahsulot sotuvi" (Daromad).
  - "Dastgoh", "Zapchast", "Remont" -> "Uskuna va Ta'mirlash" (Xarajat).
  - "Svet (Sex)", "Gaz (Sex)" -> "Kommunal (Ishlab chiqarish)" (Xarajat).
  - "Transport", "Yo'l kira" -> "Logistika" (Xarajat).
  - Muhim: "Ishlab chiqarish xarajati" deb umumiy yozma. Aniq "Xom-ashyo" yoki "Ish haqi" deb ajrat.
"""

        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        yesterday_str = (today - timedelta(days=1)).strftime('%Y-%m-%d')

        system_prompt = f"""Sen Professional Moliyaviy Tahlilchi AI assistantsan.
Sening vazifang: Berilgan matnni chuqur tahlil qilib, moliyaviy tranzaksiyalarni aniqlash va strukturalash.

MUHIM: Barcha javoblar FAQAT O'ZBEK TILIDA bo'lishi shart. Ingliz tilida yozma!

BIZNES TURI: {biz_context}

TIzimli fikrlash (Chain of Thought):
1. Har bir qatorni "iflos" (raw) ma'lumot deb qabul qil va uning tunder ma'nosini top.
2. VAQTNI ANIQLASH:
   - "Bugungi sana" (Reference): {today_str}
   - Agar matnda "Bugun" so'zi bo'lsa -> {today_str}
   - Agar "Kecha" so'zi bo'lsa -> {yesterday_str}
   - Agar sana umuman yozilmagan bo'lsa -> {today_str} (Default)
   - Agar aniq sana bor bo'lsa (01.03.2026) -> O'sha sanani ol (YYYY-MM-DD formatga o'gir).
3. ENG MUHIM SAVOL: "Bu operatsiya natijasida kassaga pul KIRYAPTIMI yoki pul CHIQIB KETYAPTIMI?"
   - Pul Kirishi (Daromad, is_expense=false):
     - Kalit so'zlar: "To'lov" (o'quvchi to'lagan), "Tushum", "Savdo", "Kirim", "Sotildi".
     - Mantiq: Agar Sardor o'quv kursi uchun pul to'lagan bo'lsa, bu bizga daromad. Summa oldida minus bo'lmasa ham.
   - Pul Chiqishi (Xarajat, is_expense=true):
     - Kalit so'zlar: "Xarajat", "Oylik", "Maosh", "Arenda", "Kommunal", "Berdi", "Sotib oldi".
     - Belgilar: Summa oldida minus (-) turgan bo'lsa.
4. Kategoriya: Biznes turiga ({biz_context}) mos keladigan eng qisqa va aniq nomni tanla.

{biz_rules}

UMUMIY QOIDALAR:
- Sana formati: YYYY-MM-DD.
- Summa: Har doim musbat son qaytar (absolyut qiymat). Masalan, matnda "-300000" bo'lsa, amount: 300000 deb, is_expense: true deb belgilash kerak.
- is_expense: Yuqoridagi mantiqqa asoslanib to'g'ri belgilash. Kod aralashmaydi, SEN MAS'ULSAN.

JAVOB FORMATI (Strict JSON array):
[
  {{
    "date": "YYYY-MM-DD",
    "amount": 1000000,
    "description": "original matn",
    "category": "Kategoriya nomi",
    "is_expense": true/false,
    "is_fixed": true/false
  }}
]
Faqat JSON qaytar.
"""
        prompt = f"Matn: \"{text}\"\n\nYuqoridagi matndan tranzaksiyalarni ajratib ol."
        
        response = await self.generate(prompt, system_prompt=system_prompt, temperature=0.3)
        
        # JSON parse qilish
        try:
            import json
            cleaned = response.strip()
            # Markdown code blocklarni tozalash
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1]
            if "```" in cleaned:
                cleaned = cleaned.split("```")[0]
            
            cleaned = cleaned.strip()
            
            # Basic validation: starts with [ and ends with ]
            if not (cleaned.startswith("[") and cleaned.endswith("]")):
                 # Agar to'liq array bo'lmasa, log qilib xato qaytarish
                 print(f"LLM Raw Response (Invalid JSON): {cleaned}")
                 raise ValueError("AI JSON formatini noto'g'ri qaytardi (uzilib qoldi).")

            transactions = json.loads(cleaned)
            if not isinstance(transactions, list):
                 raise ValueError("LLM javobi kutilgan formatda emas (list).")
                 
            if not transactions:
                 raise ValueError("Matnda moliyaviy tranzaksiyalar topilmadi.")

            # --- Post-Processing & Validation (STRICT OVERRIDE) ---
            for t in transactions:
                # 1. Ensure amount is valid positive float
                if 'amount' in t:
                    try:
                         t['amount'] = abs(float(t['amount']))
                    except:
                         t['amount'] = 0.0
                
                # 2. STRICT BUSINESS LOGIC OVERRIDE
                # AI ba'zan adashadi, shuning uchun kod orqali "qattiq" tuzatamiz.
                
                desc_lower = t.get('description', '').lower()
                cat_lower = t.get('category', '').lower()
                
                # O'quv Markazi uchun
                if business_type == "oquv_markazi":
                    # Agar "kurs" yoki "to'lov" bo'lsa va bu o'qituvchiga maosh bo'lmasa -> DAROMAD
                    if ("kurs" in desc_lower or "to'lov" in desc_lower) and "maosh" not in desc_lower and "o'qituvchi" not in desc_lower:
                        t['is_expense'] = False # Majburiy Daromad
                        # Kategoriyani to'g'rilash (ixtiyoriy)
                        if "xarajat" in cat_lower: 
                            t['category'] = "O'quv kursi to'lovi"

                # Umumiy qoidalar
                if "daromad" in cat_lower or "kirim" in cat_lower or "tushum" in cat_lower:
                    t['is_expense'] = False
                
                if "xarajat" in cat_lower or "chiqim" in cat_lower:
                    t['is_expense'] = True
            
            return transactions
        except json.JSONDecodeError as je:
             print(f"JSON Decode Error: {je}")
             print(f"Bad JSON: {cleaned}")
             raise ValueError(f"AI javobini o'qib bo'lmadi (JSON Xatosi). Fayl juda murakkab yoki katta bo'lishi mumkin.")
        except Exception as e:
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

MUHIM: Barcha javoblar FAQAT O'ZBEK TILIDA bo'lishi shart. Ingliz tilida yozma!

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
        system_prompt = """Sen LQX AI - biznes egalari uchun professional moliyaviy maslahatchisan.
Sening yagona vazifang - biznes egasiga moliya, hisobotlar va biznes rivoji bo'yicha yordam berish.

MUHIM: Barcha javoblar FAQAT O'ZBEK TILIDA bo'lishi shart. Ingliz tilida yozma!

QAT'IY QOIDALAR (GUARDRAILS):
1.  MAVZU CHEGIRASI: Agar foydalanuvchi Biznes yoki Moliya mavzusiga aloqasi yo'q savol bersa (Masalan: "Ob-havo qanday?", "Sen kimsan?", "Latifa ayt", "Siyosat", "Sport"), quyidagicha javob ber:
    "Uzr, men faqat Sizning biznesingiz va moliyaviy holatingiz bo'yicha yordam bera olaman."
    Boshqa hech qanday ma'lumot bermang.
2.  SHAXSIYLIK: O'zingni faqat "LQX Moliya Tizimi" deb tanishtir.
3.  KONTEKST: Javob berishda har doim quyidagi ma'lumotlarga tayan (agar mavjud bo'lsa): Risk darajasi, Kassa uzilishi, Hisobotlar.

JAVOB USLUBI:
- O'zbek tilida.
- Qisqa va lo'nda (maksimum 3-4 jumla).
- Professional lekin samimiy.
"""
        
        # Kontekstni matnlashtirish
        context_str = "Hozirgi Biznes Holati:\n"
        
        if 'risk_level' in context_data:
            context_str += f"- Risk Darajasi: {context_data['risk_level']}\n"
        
        # Yangi: Bu oyning statistikasi
        if 'this_month_stats' in context_data:
            stats = context_data['this_month_stats']
            context_str += f"\nBu Oyning Moliyaviy Holati:\n"
            context_str += f"- Jami Daromad: {stats['total_income']:,.0f} so'm\n"
            context_str += f"- Jami Xarajat: {stats['total_expense']:,.0f} so'm\n"
            context_str += f"- Sof Foyda: {stats['net']:,.0f} so'm\n"
        
        # Yangi: Top Xarajatlar
        if 'top_expenses' in context_data and context_data['top_expenses']:
            context_str += f"\nEng Ko'p Xarajatlar (Bu Oy):\n"
            for exp in context_data['top_expenses'][:3]:  # Faqat top 3
                context_str += f"- {exp['category']}: {exp['amount']:,.0f} so'm ({exp['percentage']}%)\n"
            
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
