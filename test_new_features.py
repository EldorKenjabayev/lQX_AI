
import requests
import json
import time

BASE_URL = "http://localhost:8000"
EMAIL = "test_new@lqxai.com"
PASSWORD = "password123"

def test_new_features():
    print("\n--- Testing File Upload & Liquidity Analytics ---")
    
    # 1. Login/Register
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        print("Registering new user...")
        requests.post(f"{BASE_URL}/auth/register", json={"email": EMAIL, "password": PASSWORD, "business_type": "Savdo"})
        resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
        
    if resp.status_code != 200:
        print("Login failed")
        return

    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Token obtained. User ID: {resp.json().get('user_id')}")

    # 2. Upload CSV via new endpoint /data/upload/file
    print("\n[Test] Uploading CSV via /data/upload/file...")
    try:
        # Generate dummy CSV if not exists
        csv_content = "date,amount,description,category\n2025-01-01,-100000,Food,Food\n2025-01-05,500000,Salary,Income"
        files = {'file': ('dummy.csv', csv_content, 'text/csv')}
        
        resp = requests.post(f"{BASE_URL}/data/upload/file", headers=headers, files=files)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.json()}")
    except Exception as e:
        print(f"Upload failed: {e}")

    # 3. Test Liquidity Analysis
    print("\n[Test] Running Liquidity Analysis (30 days)...")
    payload = {
        "period_days": 30,
        "initial_balance": 1000000
    }
    
    start_time = time.time()
    resp = requests.post(f"{BASE_URL}/analytics/liquidity", headers=headers, json=payload)
    end_time = time.time()
    
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        summary = data.get('summary', {})
        print(f"Liquidity Status: {summary.get('liquidity_status')}")
        print(f"Cash Gaps: {summary.get('cash_gaps_count')}")
        print(f"Recommendation: {summary.get('recommendation')}")
        print(f"Time taken: {end_time - start_time:.2f}s")
    else:
        print(f"Error: {resp.text}")

if __name__ == "__main__":
    test_new_features()
