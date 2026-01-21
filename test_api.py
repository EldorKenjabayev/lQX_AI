
import requests
import sys

BASE_URL = "http://localhost:8000"
EMAIL = "test_user_final@lqxai.com"
PASSWORD = "password123"

def run_tests():
    print(f"Testing LQX AI at {BASE_URL}...")
    
    # 1. Health Check
    try:
        resp = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Server not running: {e}")
        return

    # 2. Register
    print("\nRegistering...")
    # Biznes turi bilan ro'yxatdan o'tish
    register_data = {
        "email": "test_biz_uzb@lqxai.com", 
        "password": PASSWORD,
        "business_type": "O'quv markazi"
    }
    resp = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if resp.status_code == 200:
        print("Register Success")
    elif resp.status_code == 400 and "allaqachon" in resp.text:
        print("User already exists")
    else:
        print(f"Register Failed: {resp.status_code} - {resp.text}")

    # 3. Login
    print("\nLogging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": "test_biz_uzb@lqxai.com", "password": PASSWORD})
    if resp.status_code != 200:
        print(f"Login Failed: {resp.status_code} - {resp.text}")
        return
    
    token_data = resp.json()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Login Success. Token obtained.")

    # 4. Upload CSV
    print("\nUploading CSV...")
    try:
        files = {'file': open('oquv_markazi_2_yillik_XATOLI_data.csv', 'rb')}
        resp = requests.post(f"{BASE_URL}/data/upload/csv", headers=headers, files=files)
        print(f"Upload Status: {resp.status_code}")
        print(f"Upload Response: {resp.json()}")
    except FileNotFoundError:
        print("CSV file not found, skipping upload test")

    # 5. Run Forecast
    print("\nRunning Forecast...")
    resp = requests.post(f"{BASE_URL}/forecast/run", headers=headers, json={"initial_balance": 1000000, "forecast_days": 60})
    print(f"Forecast Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Forecast Success!")
        print(f"Response Keys: {data.keys()}")
        print(f"Risk Level: {data.get('risk_level')}")
        
        # New Features Check
        cash_gaps = data.get('cash_gaps', [])
        stress_test = data.get('stress_test', {})
        
        print(f"Cash Gaps Detected: {len(cash_gaps)}")
        if cash_gaps:
             print(f"First Gap: {cash_gaps[0]}")
             
        print(f"Stress Test: {stress_test.get('scenario')}")
        print(f"Stress Test Survived: {stress_test.get('is_survived')}")
        
        print(f"Recommendation: {data.get('recommendation')}")
        print(f"Data points: {len(data.get('forecast', []))}")
    else:
        print(f"Forecast Failed: {resp.text}")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Test script failed: {e}")
