import sys
import os
import pandas as pd
from datetime import datetime
import asyncio

# Add project root to path
sys.path.append(os.getcwd())

from app.domain.services.analytics_service import AnalyticsService

def test_analytics():
    print("Testing Analytics Service...")
    service = AnalyticsService()
    
    # Mock Data (based on User's description: 2026 data, Nov/Dec)
    mock_transactions = [
        {"date": "2026-11-30", "amount": 1000000, "description": "Test Income", "category": "Kirim", "is_expense": False, "is_fixed": False},
        {"date": "2026-12-01", "amount": 500000, "description": "Test Expense", "category": "Xarajat", "is_expense": True, "is_fixed": False},
        {"date": "2026-12-17", "amount": 2000000, "description": "Big Income", "category": "Kirim", "is_expense": False, "is_fixed": False},
        {"date": "2026-12-18", "amount": 300000, "description": "Small Expense", "category": "Xarajat", "is_expense": True, "is_fixed": False},
    ]
    
    # Test 'this_year' (Assuming current date is 2026-01-22)
    # Note: The service uses datetime.now(). If system time is 2026, it should work.
    
    print("\n--- Testing 'this_year' filter ---")
    result = service.get_dashboard_data(mock_transactions, filter_type='this_year')
    
    print(f"Total Income: {result['summary']['total_income']}")
    print(f"Total Expense: {result['summary']['total_expense']}")
    
    charts = result['charts']
    print(f"Chart Points Count: {len(charts)}")
    
    # Check for non-zero points
    non_zero = [p for p in charts if p['income'] > 0 or p['expense'] > 0]
    print(f"Non-zero Chart Points: {len(non_zero)}")
    for p in non_zero[:5]:
        print(f"Date: {p['date']}, Inc: {p['income']}, Exp: {p['expense']}")
        
    if len(non_zero) == 0:
        print("FAIL: No data found in chart points!")
    else:
        print("SUCCESS: Chart data populated.")

if __name__ == "__main__":
    test_analytics()
