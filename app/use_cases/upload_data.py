
from fastapi import UploadFile
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.domain.services.file_parsing_service import file_parsing_service
from app.infrastructure.llm.local_llm_client import llm_client

class UploadDataUseCase:
    """Ma'lumot yuklash va parse qilish use case."""
    
    async def parse_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Oddiy matnni tranzaksiyalarga parse qilish.
        """
        transactions = await llm_client.parse_text_to_transactions(text)
        return transactions
    
    async def parse_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Har qanday qo'llab-quvvatlanadigan faylni (CSV, XLSX, PDF, DOCX) parse qilish.
        """
        try:
            transactions = await file_parsing_service.parse_file(file)
            
            # Qo'shimcha validatsiya yoki tozalash kerak bo'lsa shu yerda
            validation = self.validate_transactions(transactions)
            if not validation['valid']:
                return {'success': False, 'error': str(validation.get('errors'))}

            return {
                "success": True,
                "transactions": transactions,
                "count": len(transactions)
            }
        except ValueError as ve:
            # Biz bilgan xatolar (masalan, format noto'g'ri, tranzaksiya yo'q)
            return {"success": False, "error": str(ve)}
        except Exception as e:
            # Kutilmagan tizim xatolari
            print(f"Upload Error: {e}")
            return {"success": False, "error": "Tizim xatosi: Faylni qayta ishlash imkonsiz."}
    
    def validate_transactions(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Tranzaksiyalarni tekshirish.
        """
        if not transactions:
            return {
                'valid': False,
                'error': 'Tranzaksiyalar ro\'yxati bo\'sh'
            }
        
        errors = []
        
        for i, txn in enumerate(transactions):
            # Date tekshirish
            if 'date' not in txn:
                errors.append(f"Tranzaksiya {i+1}: 'date' yo'q")
                continue
            
            try:
                # Agar sana formati noto'g'ri bo'lsa, try-catch
                # YYYY-MM-DD
                datetime.strptime(txn['date'], '%Y-%m-%d')
            except:
                errors.append(f"Tranzaksiya {i+1}: noto'g'ri sana formati ({txn.get('date')})")
            
            # Amount tekshirish
            if 'amount' not in txn or not isinstance(txn['amount'], (int, float)):
                errors.append(f"Tranzaksiya {i+1}: 'amount' noto'g'ri")
            
            # Description tekshirish
            if 'description' not in txn or not txn['description']:
                errors.append(f"Tranzaksiya {i+1}: 'description' bo'sh")
        
        if errors:
            return {
                'valid': False,
                'errors': errors
            }
        
        return {
            'valid': True,
            'count': len(transactions)
        }

# Global instance
upload_data_use_case = UploadDataUseCase()
