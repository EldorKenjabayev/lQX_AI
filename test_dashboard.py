
import requests
import json
import time
import random
import string

BASE_URL = "http://localhost:8000"
# Random email to ensure clean state
rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
EMAIL = f"test_{rand_str}@lqxai.com"
PASSWORD = "password123"

def test_dashboard():
    print(f"\n--- Testing Dashboard Analytics (User: {EMAIL}) ---")
    
    # 1. Register & Login
    print("Registering...")
    resp = requests.post(f"{BASE_URL}/auth/register", json={"email": EMAIL, "password": PASSWORD, "business_type": "Savdo"})
    if resp.status_code != 200:
        print(f"Register failed: {resp.text}")
        return

    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Token obtained.")

    # 1.5 Upload Data (CSV with Uzbek categories)
    print("\n[Setup] Uploading CSV (Explicit Uzbek)...")
    from datetime import datetime, timedelta
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    csv_content = f"date,amount,description,category,is_expense\n{today},500000,Maosh,Daromad,False\n{yesterday},100000,Tushlik,Oziq-ovqat,True"
    files = {'file': ('dashboard_test.csv', csv_content, 'text/csv')}
    
    upload_resp = requests.post(f"{BASE_URL}/data/upload/file", headers=headers, files=files)
    print(f"CSV Upload Status: {upload_resp.status_code}")

    # 1.6 Upload Text (AI Parsing Check)
    print("\n[Setup] Uploading Text (AI Parsing)...")
    # "Benzin" -> Transport (expected)
    text_payload = {"text": "Bugun 50000 so'm benzin quyidim"}
    text_resp = requests.post(f"{BASE_URL}/data/upload/text", headers=headers, json=text_payload)
    print(f"Text Upload Status: {text_resp.status_code}")
    if text_resp.status_code == 200:
        print(f"AI Parsed Message: {text_resp.json().get('message')}")

    # 2. Test Dashboard - This Month (to cover default AI dates)
    print("\n[Test] Dashboard (This Month)...")
    payload = {"filter_type": "this_month"}
    
    resp = requests.post(f"{BASE_URL}/analytics/dashboard", headers=headers, json=payload)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()['data']
        summary = data['summary']
        details = data.get('details', {})
        print(f"Summary: Income={summary['total_income']}, Expense={summary['total_expense']}")
        
        # Verify Amounts
        # Income: 500k (CSV)
        # Expense: 100k (CSV) + 50k (Text) = 150k
        if summary['total_expense'] == 150000:
             print("Amount Check: PASSED (150k total expense)")
        else:
             print(f"Amount Check: FAILED (Expected 150k, got {summary['total_expense']})")

        # Verify Details
        print(f"Expense Categories Breakdown: {details.get('expense_by_category', [])}")
        
        # Check Categories
        categories = [item['category'] for item in details.get('expense_by_category', [])]
        print(f"Found Expense Categories: {categories}")
        
        if 'Oziq-ovqat' in categories:
            print("CSV Localization Check: PASSED (Oziq-ovqat found)")
        else:
            print("CSV Localization Check: FAILED")
            
        # Check AI Text Parsing Result
        # We expect 'Transport' or 'Yoqilg'i' (Uzbek)
        other_cats = [c for c in categories if c != 'Oziq-ovqat']
        if other_cats:
             print(f"AI Text Parsing Check: PASSED (New category found: {other_cats})")
             # Optional: Check if it looks Uzbek (not 'Gas' or 'Fuel')
             if other_cats[0] in ['Transport', 'Yoqilg\'i', 'Transport xarajatlari']:
                 print("AI Localization Language Check: PASSED")
             else:
                 print(f"AI Localization Language Check: REVIEW NEEDED (Got {other_cats[0]})")
        else:
             print("AI Text Parsing Check: FAILED (No extra category found for Benzin)")

    else:
        print(f"Error: {resp.text}")

if __name__ == "__main__":
    test_dashboard()
