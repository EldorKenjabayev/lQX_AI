
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
        end_date: str = None
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
                
        return df

    def get_dashboard_data(self, transactions: List[Dict[str, Any]], filter_type: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Dashboard uchun tayyor ma'lumotlarni qaytaradi.
        """
        # DataFrame yaratish
        df_all = pd.DataFrame(transactions)
        
        # 1. Current Balance (Joriy Qoldiq - Barcha vaqtlar uchun)
        current_balance = 0
        if not df_all.empty:
            df_all['amount'] = pd.to_numeric(df_all['amount'])
            df_all['date'] = pd.to_datetime(df_all['date'])
            
            total_inc_all = df_all[df_all['is_expense'] == False]['amount'].sum()
            total_exp_all = df_all[df_all['is_expense'] == True]['amount'].sum()
            current_balance = total_inc_all - total_exp_all
        
        # Filterlash (df_all dan foydalanib)
        df = self.filter_transactions(df_all, filter_type, start_date, end_date)
        
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

        # Chart 2: Income vs Expense Trend
        resample_rule = 'D'
        if filter_type in ['this_year', 'last_year']:
            resample_rule = 'ME'
        
        income_trend = df[df['is_expense'] == False].set_index('date').resample(resample_rule)['amount'].sum()
        expense_trend = df[df['is_expense'] == True].set_index('date').resample(resample_rule)['amount'].sum()
        
        trend_df = pd.DataFrame({'income': income_trend, 'expense': expense_trend}).fillna(0)
        
        date_format = '%Y-%m-%d'
        if resample_rule == 'ME':
            date_format = '%Y-%m'
            
        trend_chart = {
            'categories': trend_df.index.strftime(date_format).tolist(),
            'series': [
                {'name': 'Income', 'data': trend_df['income'].tolist()},
                {'name': 'Expense', 'data': trend_df['expense'].tolist()}
            ]
        }

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

        return {
            "current_balance": float(current_balance),
            "growth_percentage": round(growth_percentage, 1),
            "top_expenses": top_expenses,
            "summary": {
                "total_income": float(total_income),
                "total_expense": float(total_expense),
                "net_profit": float(net_profit),
                "avg_income": float(avg_income),
                "avg_expense": float(avg_expense)
            },
            "charts": {
                "pie_chart": pie_chart,
                "trend_chart": trend_chart
            },
            "details": {
                "income_by_category": income_details,
                "expense_by_category": expense_details
            }
        }

    def _empty_dashboard(self):
        return {
            "current_balance": 0.0,
            "growth_percentage": 0.0,
            "top_expenses": [],
            "summary": {
                "total_income": 0, "total_expense": 0, "net_profit": 0,
                "avg_income": 0, "avg_expense": 0
            },
            "charts": {
                "pie_chart": {'labels': [], 'series': []},
                "trend_chart": {'categories': [], 'series': []}
            },
            "details": {
                "income_by_category": [],
                "expense_by_category": []
            }
        }

analytics_service = AnalyticsService()
