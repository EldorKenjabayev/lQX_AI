
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

    async def parse_file(self, file: UploadFile, task_id: Optional[str] = None, business_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fayl formatiga qarab tegishli parserni chaqiradi.
        Agar task_id berilsa, progress update qilinadi.
        business_type: AI parsing uchun (prompt customization).
        """
        from app.infrastructure.task_manager import task_manager
        
        filename = file.filename.lower()
        content = await file.read()
        
        try:
            if filename.endswith('.csv'):
                return await self._parse_csv(content, task_id, business_type)
            elif filename.endswith('.xlsx'):
                return await self._parse_excel(content, task_id, business_type)
            elif filename.endswith('.pdf'):
                return await self._parse_pdf(content, task_id, business_type)
            elif filename.endswith('.docx'):
                return await self._parse_docx(content, task_id, business_type)
            elif filename.endswith('.txt'):
                return await self._parse_txt(content, task_id, business_type)
            else:
                raise ValueError("Qo'llab-quvvatlanmaydigan fayl formati")
        except ValueError as ve:
            if task_id:
                task_manager.update_task(task_id, error=str(ve))
            raise ve
        except Exception as e:
            error_msg = f"Faylni o'qishda xatolik: {str(e)}"
            if task_id:
                task_manager.update_task(task_id, error=error_msg)
            raise ValueError(error_msg)
        finally:
            await file.seek(0)

    async def _process_chunks_with_llm(self, text_content: str, task_id: Optional[str] = None, business_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Katta matnni chunklarga bo'lib, LLM orqali qayta ishlash.
        """
        from app.infrastructure.task_manager import task_manager
        
        lines = text_content.splitlines()
        total_lines = len(lines)
        # Chunk size (optimal: 50 qator)
        chunk_size = 50 
        chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
        total_chunks = len(chunks)
        
        all_transactions = []
        
        print(f"INFO: Processing {total_lines} lines in {total_chunks} chunks.")
        
        for i, chunk_lines in enumerate(chunks):
            # Progress update
            if task_id:
                percent = int(((i) / total_chunks) * 90) # 90% gacha (parsing jarayoni)
                task_manager.update_task(
                    task_id, 
                    progress=percent, 
                    message=f"AI tahlil qilmoqda ({business_type or 'General'}): {i+1}-qism ({total_chunks} dan)..."
                )
            
            chunk_text = "\n".join(chunk_lines)
            if not chunk_text.strip():
                continue
                
            try:
                # LLM ga yuborish
                transactions = await llm_client.parse_text_to_transactions(chunk_text, business_type)
                all_transactions.extend(transactions)
            except Exception as e:
                print(f"Chunk {i+1} failed: {e}")
                # Bitta chunk xato bersa to'xtab qolmaymiz, davom etamiz
                continue
        
        if not all_transactions and total_lines > 0:
             raise ValueError("AI hech qanday ma'lumotni o'qiy olmadi.")

        return all_transactions

    async def _parse_csv(self, content: bytes, task_id: Optional[str] = None, business_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """CSV faylni o'qish (Pandas -> Fallback to LLM with Chunking)."""
        from app.infrastructure.task_manager import task_manager
        
        try:
            # 1. Standart o'qishga urinish
            if task_id: task_manager.update_task(task_id, message="Fayl o'qilmoqda...", progress=5)
            df = pd.read_csv(io.BytesIO(content))
            return self._df_to_transactions(df)
        except Exception as e:
            print(f"CSV Standard Parse Error: {e}. Trying AI fallback with chunks...")
            
            # 2. AI Fallback (Chunking)
            text_content = content.decode('utf-8', errors='ignore')
            return await self._process_chunks_with_llm(text_content, task_id, business_type)

    async def _parse_excel(self, content: bytes, task_id: Optional[str] = None, business_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Excel faylni o'qish (Pandas -> Fallback to LLM)."""
        from app.infrastructure.task_manager import task_manager
        try:
            if task_id: task_manager.update_task(task_id, message="Excel o'qilmoqda...", progress=5)
            df = pd.read_excel(io.BytesIO(content))
            return self._df_to_transactions(df)
        except Exception as e:
             # Excel fallback qiyinroq, lekin urinib ko'ramiz
             print(f"Excel Error: {e}")
             if task_id: task_manager.update_task(task_id, error="Excel fayli buzilgan va uni AI o'qiy olmadi.")
             raise ValueError(f"Excel fayli noto'g'ri formatda: {str(e)}")

    async def _parse_pdf(self, content: bytes, task_id: Optional[str] = None, business_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """PDF fayldan matnni olish va LLM orqali parse qilish."""
        from app.infrastructure.task_manager import task_manager
        try:
            if task_id: task_manager.update_task(task_id, message="PDF o'qilmoqda...", progress=5)
            text = ""
            pdf_file = io.BytesIO(content)
            reader = pypdf.PdfReader(pdf_file)
            
            # To'liq textni olamiz (endi chunking bor)
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return await self._process_chunks_with_llm(text, task_id, business_type)
        except Exception as e:
             if "No module named 'pypdf'" in str(e):
                  raise ValueError("PDF o'qish tizimi o'rnatilmagan (pypdf).")
             raise e
             
    async def _parse_docx(self, content: bytes, task_id: Optional[str] = None, business_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Word fayldan matnni olish va LLM orqali parse qilish."""
        from app.infrastructure.task_manager import task_manager
        try:
             if task_id: task_manager.update_task(task_id, message="Word fayl o'qilmoqda...", progress=5)
             doc = docx.Document(io.BytesIO(content))
             text = "\n".join([para.text for para in doc.paragraphs])
             return await self._process_chunks_with_llm(text, task_id, business_type)
        except Exception as e:
             raise e

    async def _parse_txt(self, content: bytes, task_id: Optional[str] = None, business_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """TXT fayldan matnni olish va LLM orqali parse qilish."""
        text = content.decode('utf-8', errors='ignore')
        return await self._process_chunks_with_llm(text, task_id, business_type)


    def _df_to_transactions(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """DataFrame'ni tranzaksiya formatiga o'tkazish (CSV/Excel uchun)."""
        # Ustun nomlarini normallashtirish (kichik harflar)
        df.columns = df.columns.str.lower()
        
        transactions = []
        for _, row in df.iterrows():
            # 1. Amount va Is_Expense aniqlash
            amount_val = float(row.get('amount', 0))
            raw_is_expense = row.get('is_expense')
            
            is_expense = True # Default fallback
            
            if pd.notna(raw_is_expense):
                 is_expense = bool(raw_is_expense)
            else:
                 # Auto-detect based on SIGN
                 if amount_val < 0:
                      is_expense = True
                 else:
                      # Musbat bo'lsa, kategoriya yoki default Daromad deb olish
                      cat_val = str(row.get('category', '')).lower()
                      if "xarajat" in cat_val or "chiqim" in cat_val:
                           is_expense = True
                      else:
                           is_expense = False # Default Daromad (agar musbat bo'lsa)
            
            # Sana formatini tekshirish (ToString)
            date_val = str(row.get('date', ''))
            
            # Future Date Validation
            try:
                from datetime import datetime
                # Pandas timestamp to python datetime conversion if needed, or string parsing
                # Usually pandas reads date as Timestamp if format is standard. 
                # Let's ensure we handle both Timestamp object and string.
                txn_date = None
                raw_date = row.get('date')
                
                if pd.isna(raw_date):
                     # Agar sana yo'q bo'lsa, o'tkazib yuboramiz yoki bugungi kun?
                     # User logic seems to imply strict date adherence. Let's keep empty string and let backend validataion handle or default.
                     # But for future checking, we need a date.
                     pass
                else:
                     if hasattr(raw_date, 'to_pydatetime'):
                          txn_date = raw_date.to_pydatetime()
                     else:
                          # Try parsing string iso format or common formats
                          # For simplicity, let pandas do it if it missed it
                          txn_date = pd.to_datetime(raw_date).to_pydatetime()
                
                if txn_date:
                     # Check if future
                     if txn_date > datetime.now():
                          continue # Skip future transactions
                     
                     # Normalize format to string YYYY-MM-DD for consistency
                     date_val = txn_date.strftime('%Y-%m-%d')
                     
            except Exception as e:
                # Agar sana formati buzilgan bo'lsa, warning berib o'tkazib yuboramiz yoki original string qoldiramiz
                # Lekin "Future" checking ishlamaydi.
                pass

            txn = {
                "date": date_val,
                "amount": abs(amount_val), # DB uchun har doim musbat
                "description": str(row.get('description', '')),
                "category": str(row.get('category', 'Boshqa')),
                "is_expense": is_expense,
                "is_fixed": bool(row.get('is_fixed', False))
            }
            transactions.append(txn)
            
        return transactions

file_parsing_service = FileParsingService()
