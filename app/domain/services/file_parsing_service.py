
import io
import pandas as pd
from typing import List, Dict, Any, Optional
from fastapi import UploadFile
import pypdf
import docx
import openpyxl

from app.infrastructure.llm.local_llm_client import llm_client

class FileParsingService:
    """
    Turli formatdagi fayllarni o'qish va ma'lumotlarni ajratib olish servisi.
    Qo'llab-quvvatlaydi: .csv, .xlsx, .pdf, .docx, .txt
    """

    async def parse_file(self, file: UploadFile) -> List[Dict[str, Any]]:
        """
        Fayl formatiga qarab tegishli parserni chaqiradi.
        """
        filename = file.filename.lower()
        content = await file.read()
        
        try:
            if filename.endswith('.csv'):
                return self._parse_csv(content)
            elif filename.endswith('.xlsx'):
                return self._parse_excel(content)
            elif filename.endswith('.pdf'):
                return await self._parse_pdf(content) # LLM kerak bo'lishi mumkin
            elif filename.endswith('.docx'):
                return await self._parse_docx(content) # LLM kerak bo'lishi mumkin
            elif filename.endswith('.txt'):
                return await self._parse_txt(content)
            else:
                raise ValueError("Qo'llab-quvvatlanmaydigan fayl formati")
        except ValueError as ve:
            raise ve # O'zimiz ko'targan xatolarni o'tkazamiz
        except Exception as e:
            raise ValueError(f"Faylni o'qishda xatolik: {str(e)}")
        finally:
            await file.seek(0) # Faylni qayta o'qishga tayyorlash (kerak bo'lsa)

    def _parse_csv(self, content: bytes) -> List[Dict[str, Any]]:
        """CSV faylni o'qish."""
        df = pd.read_csv(io.BytesIO(content))
        return self._df_to_transactions(df)

    def _parse_excel(self, content: bytes) -> List[Dict[str, Any]]:
        """Excel faylni o'qish."""
        df = pd.read_excel(io.BytesIO(content))
        return self._df_to_transactions(df)

    async def _parse_pdf(self, content: bytes) -> List[Dict[str, Any]]:
        """PDF fayldan matnni olish va LLM orqali parse qilish."""
        text = ""
        pdf_file = io.BytesIO(content)
        reader = pypdf.PdfReader(pdf_file)
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        return await llm_client.parse_text_to_transactions(text)

    async def _parse_docx(self, content: bytes) -> List[Dict[str, Any]]:
        """Word fayldan matnni olish va LLM orqali parse qilish."""
        doc = docx.Document(io.BytesIO(content))
        text = "\n".join([para.text for para in doc.paragraphs])
        return await llm_client.parse_text_to_transactions(text)

    async def _parse_txt(self, content: bytes) -> List[Dict[str, Any]]:
        """TXT fayldan matnni olish va LLM orqali parse qilish."""
        text = content.decode('utf-8')
        return await llm_client.parse_text_to_transactions(text)

    def _df_to_transactions(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """DataFrame'ni tranzaksiya formatiga o'tkazish (CSV/Excel uchun)."""
        # Ustun nomlarini normallashtirish (kichik harflar)
        df.columns = df.columns.str.lower()
        
        required_cols = ['date', 'amount', 'description']
        # Agar kerakli ustunlar bo'lmasa, xato qaytarish yoki boshqa logika o'ylash kerak
        # Hozircha oddiy mapping
        
        transactions = []
        for _, row in df.iterrows():
            # Sana formatini tekshirish kerak bo'lishi mumkin
            txn = {
                "date": str(row.get('date', '')),
                "amount": float(row.get('amount', 0)),
                "description": str(row.get('description', '')),
                "category": str(row.get('category', 'Boshqa')),
                "is_expense": bool(row.get('is_expense', True)),
                "is_fixed": bool(row.get('is_fixed', False))
            }
            transactions.append(txn)
            
        return transactions

file_parsing_service = FileParsingService()
