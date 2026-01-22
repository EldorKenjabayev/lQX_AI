
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta

class AnalyticsService:
    """
    Dashboard analitikasi va ma'lumotlarni agregatsiya qilish servisi.
    """

    def filter_transactions(
        self, 
        df: pd.DataFrame, 
        filter_type: str, 
        start_date: str = None, 
        end_date: str = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Tranzaksiyalarni vaqt bo'yicha filtrlash.
        """
        if df.empty:
            return df

        # Hozirgi sana
        now = datetime.now()
        
        # Filtrlash mantiqi
        if filter_type == 'last_7_days':
            cutoff = now - timedelta(days=7)
            df = df[df['date'] >= cutoff]
        elif filter_type == 'this_month':
            cutoff = now.replace(day=1)
            df = df[df['date'] >= cutoff]
        elif filter_type == 'last_month':
            first_day_this_month = now.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            df = df[(df['date'] >= first_day_last_month) & (df['date'] <= last_day_last_month)]
        elif filter_type == 'this_year':
            cutoff = now.replace(month=1, day=1)
            df = df[df['date'] >= cutoff]
        elif filter_type == 'custom':
            if start_date:
                df = df[df['date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['date'] <= pd.to_datetime(end_date)]
        
        # Additional filters
        if 'category' in kwargs and kwargs['category']:
            df = df[df['category'] == kwargs['category']]
            
        if 'min_amount' in kwargs and kwargs['min_amount'] is not None:
             df = df[df['amount'] >= float(kwargs['min_amount'])]
             
        if 'max_amount' in kwargs and kwargs['max_amount'] is not None:
             df = df[df['amount'] <= float(kwargs['max_amount'])]
                
        return df

    def get_dashboard_data(self, transactions: List[Dict[str, Any]], filter_type: str, start_date: str = None, end_date: str = None, **kwargs) -> Dict[str, Any]:
        """
        Dashboard uchun tayyor ma'lumotlarni qaytaradi.
        """
        # DataFrame yaratish
        df_all = pd.DataFrame(transactions)
        
        # Ensure date column is datetime objects for comparison
        if not df_all.empty and 'date' in df_all.columns:
            df_all['date'] = pd.to_datetime(df_all['date'])
        
        # 1. Current Balance (Joriy Qoldiq - Barcha vaqtlar uchun)
        # 1. Real Current Balance (Joriy Qoldiq - Barcha vaqtlar uchun, filtrlardan qat'iy nazar)
        current_balance = 0
        if not df_all.empty:
            # Type casting agar kerak bo'lsa
            # df_all['amount'] = pd.to_numeric(df_all['amount']) # bular allaqachon float bo'lishi kerak
            
            # Real balansni hisoblash (barcha tranzaksiyalar)
            total_inc_all = df_all[df_all['is_expense'] == False]['amount'].sum()
            total_exp_all = df_all[df_all['is_expense'] == True]['amount'].sum()
            current_balance = total_inc_all - total_exp_all
        
        # Filterlash (df_all dan foydalanib)
        df = self.filter_transactions(df_all, filter_type, start_date, end_date, **kwargs)
        
        if df.empty:
             empty = self._empty_dashboard()
             empty['current_balance'] = float(current_balance)
             return empty

        # Asosiy ko'rsatkichlar (KPIs)
        total_income = df[df['is_expense'] == False]['amount'].sum()
        total_expense = df[df['is_expense'] == True]['amount'].sum()
        net_profit = total_income - total_expense
        
        # O'rtacha ko'rsatkichlar
        avg_income = df[df['is_expense'] == False]['amount'].mean() if not df[df['is_expense'] == False].empty else 0
        avg_expense = df[df['is_expense'] == True]['amount'].mean() if not df[df['is_expense'] == True].empty else 0

        # 2. Growth Percentage (O'sish dinamikasi)
        growth_percentage = 0.0
        try:
            # O'tgan davrni aniqlash
            prev_start = None
            prev_end = None
            now = datetime.now()
            
            if filter_type == 'this_month':
                # O'tgan oy
                first_this = now.replace(day=1)
                prev_end = first_this - timedelta(days=1)
                prev_start = prev_end.replace(day=1)
            elif filter_type == 'last_7_days':
                # Oldingi 7 kun
                start_curr = now - timedelta(days=7)
                prev_end = start_curr - timedelta(days=1)
                prev_start = prev_end - timedelta(days=7)
            
            if prev_start and prev_end and not df_all.empty:
                prev_df = df_all[(df_all['date'] >= prev_start) & (df_all['date'] <= prev_end)]
                prev_income = prev_df[prev_df['is_expense'] == False]['amount'].sum()
                
                if prev_income > 0:
                    growth_percentage = ((total_income - prev_income) / prev_income) * 100
                elif total_income > 0:
                    growth_percentage = 100.0
        except Exception as e:
            print(f"Growth calc error: {e}")

        # Chart 1: Categories Breakdown (Pie Chart) - Faqat xarajatlar
        expenses_df = df[df['is_expense'] == True]
        if not expenses_df.empty:
            cat_groups = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
            pie_chart = {
                'labels': cat_groups.index.tolist(),
                'series': cat_groups.values.tolist()
            }
        else:
            pie_chart = {'labels': [], 'series': []}

        # Chart 2: Income vs Expense Trend (List[ChartPoint]) - Full Date Range Logic
        resample_rule = 'D'
        date_format = '%Y-%m-%d'
        
        # Sana oraliqlarini aniqlash (to'liq chart chizish uchun)
        now = datetime.now()
        chart_start_date = now - timedelta(days=30) # Default
        chart_end_date = now

        if filter_type == 'last_7_days':
            chart_end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            chart_start_date = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif filter_type == 'this_month':
            # Oyning boshi va oxiri
            chart_start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Find last day of month
            next_month = now.replace(day=28) + timedelta(days=4)
            chart_end_date = (next_month - timedelta(days=next_month.day)).replace(hour=23, minute=59, second=59, microsecond=999999)
            
        elif filter_type == 'last_month':
            first_this = now.replace(day=1)
            chart_end_date = (first_this - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
            chart_start_date = chart_end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif filter_type == 'custom' and start_date and end_date:
            chart_start_date = pd.to_datetime(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
            chart_end_date = pd.to_datetime(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)

        # Fix for 'this_year' specifically
        if filter_type == 'this_year':
             resample_rule = 'ME' # Reduce to 12 points as user requested "not squeezed"
             date_format = '%b'   # Show Month Name (Jan, Feb...)
             chart_start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
             chart_end_date = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        
        # Override specifically to fix the bug (redundant block removed, merged above)

        # Full date range yaratish
        full_idx = pd.date_range(start=chart_start_date, end=chart_end_date, freq=resample_rule)
        
        # Resample and fill missing dates with 0 via reindex
        # 1. Group by date and sum
        if not df.empty:
             # Create a dedicated chart dataframe to avoid SettingWithCopyWarning
             chart_df = df.copy()
             chart_df['date'] = pd.to_datetime(chart_df['date'])
             
             # Normalize chart_df dates to remove any potential time part (crucial!)
             # For Monthly resampling, normalize is good but resample('ME') handles days automatically.
             # However, let's keep it clean.
             chart_df['date'] = chart_df['date'].dt.normalize()

             income_grouped = chart_df[chart_df['is_expense'] == False].set_index('date').resample(resample_rule)['amount'].sum()
             expense_grouped = chart_df[chart_df['is_expense'] == True].set_index('date').resample(resample_rule)['amount'].sum()
             
             # 2. Reindex with full range
             # Normalize full_idx just in case? pd.date_range with start/end normalized should be creating normalized range if freq=D.
             # But our fix above ensures start/end are normalized.
             
             income_trend = income_grouped.reindex(full_idx, fill_value=0)
             expense_trend = expense_grouped.reindex(full_idx, fill_value=0)
        else:
             # Agar df bo'sh bo'lsa, hammasi 0 bo'lgan series yaratamiz
             income_trend = pd.Series(0, index=full_idx)
             expense_trend = pd.Series(0, index=full_idx)
        
        trend_df = pd.DataFrame({'income': income_trend, 'expense': expense_trend})
        trend_df['net_change'] = trend_df['income'] - trend_df['expense']
        
        chart_points = []
        for date, row in trend_df.iterrows():
            chart_points.append({
                "date": date.strftime(date_format),
                "income": float(row['income']),
                "expense": float(row['expense']),
                "net_change": float(row['net_change'])
            })

        # Details helpers
        def get_category_details(sub_df, total):
            if sub_df.empty or total == 0:
                return []
            groups = sub_df.groupby('category')['amount'].sum().sort_values(ascending=False)
            details = []
            for cat, amount in groups.items():
                details.append({
                    'category': cat,
                    'amount': float(amount),
                    'percentage': round((amount / total) * 100, 1)
                })
            return details

        income_details = get_category_details(df[df['is_expense'] == False], total_income)
        expense_details = get_category_details(df[df['is_expense'] == True], total_expense)

        # 3. Top Expenses (Top 3)
        top_expenses = expense_details[:3]
        
        # Calculate daily averages (non-zero days only or total period?)
        # User wants "Linear AVG". total / period_length seems appropriate for visual reference.
        # Or better: average of non-zero days? Usually financial planning uses total / days.
        # Let's use simple average over the period.
        period_days = (chart_end_date - chart_start_date).days + 1
        avg_daily_income = total_income / period_days if period_days > 0 else 0
        avg_daily_expense = total_expense / period_days if period_days > 0 else 0

        return {
            "current_balance": float(current_balance),
            "growth_percentage": round(growth_percentage, 1),
            "top_expenses": top_expenses,
            "summary": {
                "total_income": float(total_income),
                "total_expense": float(total_expense),
                "net_profit": float(net_profit),
                "savings_rate": round(((total_income - total_expense) / total_income * 100), 1) if total_income > 0 else 0.0,
            },
            "charts": chart_points,
            "details": {
                "income_by_category": income_details,
                "expense_by_category": expense_details,
                "avg_stats": {
                    "daily_income": float(avg_daily_income),
                    "daily_expense": float(avg_daily_expense)
                }
            }
        }

    def _empty_dashboard(self):
        return {
            "current_balance": 0.0,
            "growth_percentage": 0.0,
            "top_expenses": [],
            "summary": {
                "total_income": 0, "total_expense": 0, "net_profit": 0, "savings_rate": 0
            },
            "charts": [],
            "details": {
                "income_by_category": [],
                "expense_by_category": []
            }
        }

    def get_filter_options(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Tranzaksiyalardan filtrlash uchun kerakli ma'lumotlarni yig'adi.
        """
        df = pd.DataFrame(transactions)
        
        if df.empty:
            return {
                "categories": [],
                "min_date": None,
                "max_date": None,
                "min_amount": 0.0,
                "max_amount": 0.0
            }
            
        # Kategoriyalar (faqat string bo'lganlarini va bo'sh bo'lmaganlarini olish)
        categories = df['category'].dropna().unique().tolist()
        categories.sort()
        
        # Sanalar check
        df['date'] = pd.to_datetime(df['date'])
        min_date = df['date'].min().strftime('%Y-%m-%d')
        max_date = df['date'].max().strftime('%Y-%m-%d')
        
        # Summalar
        df['amount'] = pd.to_numeric(df['amount'])
        min_amount = float(df['amount'].min())
        max_amount = float(df['amount'].max())
        
        return {
            "categories": categories,
            "min_date": min_date,
            "max_date": max_date,
            "min_amount": min_amount,
            "max_amount": max_amount
        }

analytics_service = AnalyticsService()
