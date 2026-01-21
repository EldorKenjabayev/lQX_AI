"""
Domain Service - Forecasting Service

Gibrid prognozlash logikasi (Prophet vs Cash Flow Simulation).
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from decimal import Decimal


class ForecastingService:
    """Likvidlik prognozlash xizmati."""
    
    def __init__(self):
        self.min_days_for_timeseries = 90
    
    def prepare_data(self, transactions: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Tranzaksiyalarni prognoz uchun tayyorlash.
        
        Args:
            transactions: Tranzaksiyalar ro'yxati
            
        Returns:
            Pandas DataFrame
        """
        df = pd.DataFrame(transactions)
        
        if df.empty:
            return df
        
        # Date ustunini datetime'ga aylantirish
        df['date'] = pd.to_datetime(df['date'])
        
        # Amount'ni float'ga
        df['amount'] = df['amount'].astype(float)
        
        # Signed amount (daromad +, xarajat -)
        df['signed_amount'] = df.apply(
            lambda row: -row['amount'] if row.get('is_expense', True) else row['amount'],
            axis=1
        )
        
        # Sanaga qarab saralash
        df = df.sort_values('date')
        
        return df
    
    def calculate_daily_balance(self, df: pd.DataFrame, initial_balance: float = 0) -> pd.DataFrame:
        """
        Kunlik balansni hisoblash.
        
        Args:
            df: Tayyorlangan DataFrame
            initial_balance: Boshlang'ich balans
            
        Returns:
            Kunlik balans bilan DataFrame
        """
        # Kunlik umumiy tranzaksiyalarni hisoblash
        daily_df = df.groupby('date')['signed_amount'].sum().reset_index()
        daily_df.columns = ['date', 'daily_change']
        
        # Kumulyativ balans
        daily_df['balance'] = initial_balance + daily_df['daily_change'].cumsum()
        
        return daily_df
    
    def forecast_with_prophet(
        self,
        df: pd.DataFrame,
        forecast_days: int = 90
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Prophet yordamida time-series prognoz.
        
        Args:
            df: Kunlik balans DataFrame
            forecast_days: Prognoz kunlari
            
        Returns:
            Prognoz DataFrame va metadata
        """
        try:
            from prophet import Prophet
            
            # Prophet uchun format
            prophet_df = df[['date', 'balance']].copy()
            prophet_df.columns = ['ds', 'y']
            
            # Model
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=True,
                changepoint_prior_scale=0.05
            )
            model.fit(prophet_df)
            
            # Future dates
            future = model.make_future_dataframe(periods=forecast_days)
            forecast = model.predict(future)
            
            # Faqat kelajak kunlarni olish
            forecast_only = forecast[forecast['ds'] > df['date'].max()].copy()
            forecast_only = forecast_only[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            forecast_only.columns = ['date', 'predicted_balance', 'lower_bound', 'upper_bound']
            
            metadata = {
                'method': 'prophet',
                'history_days': len(df),
                'forecast_days': forecast_days
            }
            
            return forecast_only, metadata
            
        except Exception as e:
            print(f"Prophet xatosi: {str(e)}")
            return pd.DataFrame(), {'method': 'prophet', 'error': str(e)}
    
    def forecast_with_simulation(
        self,
        df: pd.DataFrame,
        forecast_days: int = 90
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Cash Flow Simulation (tashqi omillar/mavsumiylik bilan).
        """
        if df.empty:
            return pd.DataFrame(), {'method': 'simulation', 'error': 'No data'}
        
        # O'rtacha kunlik o'zgarish
        avg_daily_change = df['balance'].diff().mean()
        
        # Tashqi faktor: Agar ma'lumot kam bo'lsa, konservativ yondashuv (xavfsizlik uchun)
        # Masalan, o'rtacha o'sishni biroz pasaytirish (risk buffer)
        adjusted_growth = avg_daily_change * 0.9  # 10% conservative buffer
        
        # Oxirgi balans
        last_balance = df['balance'].iloc[-1]
        last_date = df['date'].iloc[-1]
        
        # Prognoz
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_days)
        
        predicted_balances = []
        current_val = last_balance
        
        for i in range(forecast_days):
            # Oddiy mavsumiylik simulatsiyasi (sinusoida) - bozor tebranishi
            # 30 kunlik sikl
            seasonality_factor = 1 + 0.05 * np.sin(2 * np.pi * i / 30)
            
            # Keyingi kun balansi
            current_val += adjusted_growth * seasonality_factor
            predicted_balances.append(current_val)
        
        forecast_df = pd.DataFrame({
            'date': future_dates,
            'predicted_balance': predicted_balances,
            'lower_bound': [b * 0.85 for b in predicted_balances],  # Kengroq diapazon (risk)
            'upper_bound': [b * 1.15 for b in predicted_balances]
        })
        
        metadata = {
            'method': 'simulation_v2',
            'avg_daily_change': avg_daily_change,
            'history_days': len(df),
            'market_context': 'conservative_with_seasonality'
        }
        
        return forecast_df, metadata
    
    def run_forecast(
        self,
        transactions: List[Dict[str, Any]],
        initial_balance: float = 0,
        forecast_days: int = 90
    ) -> Dict[str, Any]:
        """
        Asosiy prognoz funksiyasi (gibrid).
        
        Args:
            transactions: Tranzaksiyalar ro'yxati
            initial_balance: Boshlang'ich balans
            forecast_days: Prognoz kunlari
            
        Returns:
            Prognoz natijalari
        """
        # Ma'lumotni tayyorlash
        df = self.prepare_data(transactions)
        
        if df.empty:
            return {
                'success': False,
                'error': 'Ma\'lumot yetarli emas',
                'forecast': []
            }
        
        # Kunlik balans
        daily_df = self.calculate_daily_balance(df, initial_balance)
        
        # Tarix uzunligini tekshirish
        history_days = len(daily_df)
        
        # Gibrid yondashuv
        if history_days >= self.min_days_for_timeseries:
            forecast_df, metadata = self.forecast_with_prophet(daily_df, forecast_days)
            # Agar Prophet xato bersa, Simulation'ga o'tish
            if forecast_df.empty and 'error' in metadata:
                print(f"Prophet failed, falling back to simulation: {metadata['error']}")
                forecast_df, metadata = self.forecast_with_simulation(daily_df, forecast_days)
                metadata['fallback'] = True
        else:
            forecast_df, metadata = self.forecast_with_simulation(daily_df, forecast_days)
        
        if forecast_df.empty:
            return {
                'success': False,
                'error': 'Prognoz yaratishda xato',
                'metadata': metadata
            }
        
        # Natijalarni dict'ga aylantirish
        forecast_list = forecast_df.to_dict('records')
        
        # Date'larni string'ga
        for item in forecast_list:
            item['date'] = item['date'].strftime('%Y-%m-%d')
        
        return {
            'success': True,
            'forecast': forecast_list,
            'metadata': metadata,
            'current_balance': float(daily_df['balance'].iloc[-1])
        }

    def predict_cash_flow(
        self,
        df: pd.DataFrame,
        initial_balance: float = 0,
        days: int = 90
    ) -> pd.DataFrame:
        """
        Likvidlik analizi uchun prognoz qaytaruvchi yordamchi metod.
        """
        # Agar df da 'signed_amount' yo'q bo'lsa (raw transactions), uni tayyorlash kerak.
        # Lekin LiquidityAnalysisUseCase da biz shunchaki DataFrame(transactions) qilib yubordik.
        # U yerda prepare_data ni chaqirish kerak edi yoki bu yerda handle qilish kerak.
        
        # Agar 'signed_amount' bo'lmasa, prepare_data ni chaqiramiz (lekin u dict list kutadi)
        # Keling, df ni list of dicts ga o'girib prepare_data qilamiz yoki logikani takrorlaymiz.
        # Yaxshirog'i, bu yerda logikani takrorlaymiz.
        
        if 'signed_amount' not in df.columns:
            # Simple preparation
            df['date'] = pd.to_datetime(df['date'])
            df['amount'] = pd.to_numeric(df['amount'])
            df['signed_amount'] = df.apply(
                lambda row: -row['amount'] if row.get('is_expense', True) else row['amount'],
                axis=1
            )
            df = df.sort_values('date')

        daily_df = self.calculate_daily_balance(df, initial_balance)
        history_days = len(daily_df)
        
        if history_days >= self.min_days_for_timeseries:
            forecast_df, metadata = self.forecast_with_prophet(daily_df, days)
            if forecast_df.empty and 'error' in metadata:
                 forecast_df, metadata = self.forecast_with_simulation(daily_df, days)
        else:
            forecast_df, metadata = self.forecast_with_simulation(daily_df, days)
            
        return forecast_df

    def detect_cash_gaps(self, forecast_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Kassa uzilishlarini (Cash Gaps) aniqlash.
        Qaysi sanalarda balans manfiy bo'lishini ko'rsatadi.
        """
        if forecast_df.empty:
            return []
            
        gaps = []
        for _, row in forecast_df.iterrows():
            if row['predicted_balance'] < 0:
                gaps.append({
                    'date': row['date'].strftime('%Y-%m-%d') if isinstance(row['date'], pd.Timestamp) else str(row['date']),
                    'amount': float(row['predicted_balance']),
                    'deficit': abs(float(row['predicted_balance']))
                })
        return gaps

    def run_stress_test(self, df: pd.DataFrame, forecast_days: int = 90) -> Dict[str, Any]:
        """
        Stress Test: Pessimistik ssenariy.
        Daromad -20%, Xarajat +10%.
        """
        if df.empty:
            return {'status': 'failed', 'reason': 'no_data'}
            
        daily_changes = df['balance'].diff().dropna()
        
        # Kirimlar va Chiqimlar o'rtachasi
        avg_inflow = daily_changes[daily_changes > 0].mean() if not daily_changes[daily_changes > 0].empty else 0
        avg_outflow = daily_changes[daily_changes < 0].mean() if not daily_changes[daily_changes < 0].empty else 0
        
        # Stress ssenariy parametrlari
        stressed_inflow = avg_inflow * 0.80  # Daromad 20% ga kamaydi
        stressed_outflow = avg_outflow * 1.10  # Xarajat 10% ga oshdi
        
        # Net change stress holatida
        stressed_daily_change = stressed_inflow + stressed_outflow # outflow manfiy son
        
        # Prognoz
        last_balance = df['balance'].iloc[-1]
        
        predicted_balances = []
        current_val = last_balance
        min_balance = last_balance
        
        for i in range(forecast_days):
            current_val += stressed_daily_change
            predicted_balances.append(current_val)
            if current_val < min_balance:
                min_balance = current_val
                
        is_survived = min_balance >= 0
        
        return {
            'is_survived': bool(is_survived),
            'min_balance': float(min_balance),
            'stressed_daily_change': float(stressed_daily_change),
            'scenario': 'Revenue -20%, Expense +10%'
        }

    def detect_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Xarajatlar anomaliyasini aniqlash.
        Masalan, bir kategoriya bo'yicha xarajat keskin oshgan bo'lsa.
        """
        if df.empty or 'category' not in df.columns:
            return []
            
        anomalies = []
        
        # Xarajatlarni filtrlash
        expenses = df[df['signed_amount'] < 0].copy()
        if expenses.empty:
            return []
            
        # Kategoriyalar bo'yicha guruhlash
        # Bizda vaqt seriyasi kerak, shuning uchun oxirgi 30 kun va oldingi 30 kunni solishtiramiz
        
        last_date = df['date'].max()
        cutoff_date = last_date - timedelta(days=30)
        
        current_period = expenses[expenses['date'] > cutoff_date]
        prev_period = expenses[(expenses['date'] <= cutoff_date) & (expenses['date'] > cutoff_date - timedelta(days=30))]
        
        if prev_period.empty:
            return [] # Solishtirish uchun ma'lumot yo'q
            
        current_stats = current_period.groupby('category')['amount'].sum().abs()
        prev_stats = prev_period.groupby('category')['amount'].sum().abs()
        
        for category, current_amount in current_stats.items():
            prev_amount = prev_stats.get(category, 0)
            
            if prev_amount > 0:
                change_pct = (current_amount - prev_amount) / prev_amount
                
                # Agar 20% dan ko'p oshgan bo'lsa
                if change_pct > 0.20:
                    anomalies.append({
                        'category': category,
                        'current_amount': float(current_amount),
                        'prev_amount': float(prev_amount),
                        'change_pct': float(change_pct),
                        'message': f"{category} xarajatlari o'tgan oyga nisbatan {change_pct*100:.1f}% ga oshdi."
                    })
            elif current_amount > 1000000: # Agar oldin bo'lmagan va 1 mln dan ko'p bo'lsa
                 anomalies.append({
                        'category': category,
                        'current_amount': float(current_amount),
                        'prev_amount': 0.0,
                        'change_pct': 1.0,
                        'message': f"{category} bo'yicha yangi katta xarajat: {current_amount:,.0f} so'm."
                    })
                    
        return anomalies

    def check_liquidity(self, forecast_df: pd.DataFrame, expense_amount: float) -> Dict[str, Any]:
        """
        Katta xarajat qilish mumkinligini tekshirish ("Mashina olsam bo'ladimi?").
        """
        if forecast_df.empty:
            return {'allowed': False, 'reason': 'no_forecast'}
            
        # Agar xarajat qilinsa, balans qanday o'zgaradi?
        min_projected_balance = forecast_df['predicted_balance'].min()
        
        # Xarajatdan keyingi eng past balans
        balance_after_expense = min_projected_balance - expense_amount
        
        if balance_after_expense < 0:
            return {
                'allowed': False,
                'max_affordable': float(min_projected_balance * 0.8), # 20% buffer
                'deficit': float(abs(balance_after_expense)),
                'reason': "Kassa uzilishi xavfi bor",
                'message': f"Hozirgi holatda bu xarajatni qilish xavfli. Siz maksimal {min_projected_balance * 0.8:,.0f} so'm sarflashingiz mumkin."
            }
        else:
            return {
                'allowed': True,
                'remaining_buffer': float(balance_after_expense),
                'reason': "Likvidlik yetarli",
                'message': "Ha, bu xarajatni bemalol qilishingiz mumkin. Moliyaviy holatingiz barqaror qoladi."
            }


# Global instance
forecasting_service = ForecastingService()


# Global instance
forecasting_service = ForecastingService()


