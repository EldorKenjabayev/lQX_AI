
import requests
import json
import random
import string
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
EMAIL = f"test_dash_{rand_str}@lqxai.com"
PASSWORD = "password123"

def test_dashboard_enhancements():
    print(f"\n--- Testing Dashboard Enhancements (User: {EMAIL}) ---")
    
    # 1. Register & Login
    requests.post(f"{BASE_URL}/auth/register", json={"email": EMAIL, "password": PASSWORD, "business_type": "Savdo"})
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Upload Data
    # 3 ta daromad (10m)
    # 2 ta xarajat (2m ovqat, 3m ijara)
    # Balance: 10 - 5 = 5m
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    csv = f"""date,amount,description,category,is_expense
{today},10000000,Sotuv,Daromad,False
{today},2000000,Bozor,Oziq-ovqat,True
{yesterday},3000000,Ofis,Ijara,True
"""
    files = {'file': ('test.csv', csv, 'text/csv')}
    upload_resp = requests.post(f"{BASE_URL}/data/upload/file", headers=headers, files=files)
    print(f"Upload: {upload_resp.status_code}")

    # 3. Get Dashboard
    resp = requests.post(f"{BASE_URL}/analytics/dashboard", headers=headers, json={"filter_type": "this_month"})
    
    if resp.status_code == 200:
        data = resp.json()['data']
        print(f"Response Keys: {data.keys()}")
        
        balance = data.get('current_balance')
        top = data.get('top_expenses')
        growth = data.get('growth_percentage')
        
        print(f"Current Balance: {balance} (Expected: 5000000.0)")
        print(f"Top Expenses Length: {len(top)} (Expected: 2)")
        if top:
            print(f"Top 1: {top[0]['category']} - {top[0]['amount']}")
        
        if balance == 5000000.0:
            print("Balance Check: PASSED")
        else:
            print(f"Balance Check: FAILED (Got {balance})")
            
        if len(top) == 2 and top[0]['category'] == 'Ijara':
             print("Top Expenses Check: PASSED (Ijara is top)")
        else:
             print("Top Expenses Check: FAILED or Unexpected order")
             
    else:
        print(f"Error: {resp.text}")

if __name__ == "__main__":
    test_dashboard_enhancements()
