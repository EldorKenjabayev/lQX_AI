
import requests
import json
import pandas as pd
import time

BASE_URL = "http://localhost:8000"
EMAIL = "test_biz_uzb@lqxai.com"
PASSWORD = "strongpassword123"

def run_test(file_path, business_type):
    print(f"\n--- Testing for: {business_type} ({file_path}) ---")
    
    # Register (agar login o'xshamasa)
    print("Registering/Logging in...")
    reg_payload = {"email": EMAIL, "password": PASSWORD, "business_type": business_type}
    requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
    
    # Login
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        print(f"Login Failed: {resp.text}")
        return
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Upload CSV
    print(f"Uploading {file_path}...")
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'text/csv')}
        resp = requests.post(f"{BASE_URL}/data/upload/csv", headers=headers, files=files)
        
    if resp.status_code == 200:
        print("Upload Success")
        print(resp.json())
    else:
        print(f"Upload Failed: {resp.text}")
        return

    # Run Forecast
    print("Running Forecast...")
    # Biznes turini update qilish (agar API da shunday endpoint bo'lmasa, hozircha login qilingan user settings'ida qoladi)
    # Biznes konteksti forecast paytida emas, tavsiya paytida ishlatiladi.
    # Keling, forecast so'rovini yuboramiz.
    
    forecast_payload = {
        "initial_balance": 10000000, # 10 mln boshlang'ich balans
        "forecast_days": 30
    }
    
    resp = requests.post(f"{BASE_URL}/forecast/run", headers=headers, json=forecast_payload)
    
    if resp.status_code == 200:
        data = resp.json()
        print("\nForecast/Analysis Result:")
        print(f"Risk Level: {data.get('risk_level')}")
        print(f"Algorithm Used: {data.get('metadata', {}).get('method')}")
        
        cash_gaps = data.get('cash_gaps', [])
        print(f"Cash Gaps: {len(cash_gaps)}")
        if cash_gaps:
             print(f"First Gap: {cash_gaps[0]}")
             
        stress = data.get('stress_test', {})
        print(f"Stress Test (Revenue -20%, Expense +10%): Survived? {stress.get('is_survived')}")
        print(f"Stress Min Balance: {stress.get('min_balance'):,.0f}")
        
        print("\nAI Recommendation:")
        print(data.get('recommendation'))
    else:
        print(f"Forecast Failed: {resp.text}")

if __name__ == "__main__":
    # Test Edu Center
    run_test("edu_center_2026.csv", "O'quv Markazi")
    
    # Test Restaurant
    run_test("restaurant_2026.csv", "Milliy Taomlar")
