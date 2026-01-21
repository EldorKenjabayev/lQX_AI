
import requests
import json
import random
import string

BASE_URL = "http://localhost:8000"
# Random email to ensure clean state
rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
EMAIL = f"test_err_{rand_str}@lqxai.com"
PASSWORD = "password123"

def test_error_handling():
    print(f"\n--- Testing Error Handling (User: {EMAIL}) ---")
    
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

    # 2. Upload Invalid Text
    print("\n[Test] Uploading Invalid Text (Should fail gracefully)...")
    # "Mening mushugim bor" -> No financial data
    text_payload = {"text": "Mening mushugim juda chiroyli va aqlli."}
    
    text_resp = requests.post(f"{BASE_URL}/data/upload/text", headers=headers, json=text_payload)
    print(f"Status: {text_resp.status_code}")
    print(f"Response: {text_resp.text}")
    
    try:
        resp_json = text_resp.json()
        if not resp_json.get('success'):
            print("Check PASSED: Success is False as expected.")
            if "topilmadi" in resp_json.get('error', '').lower() or "tahlil qilib bo'lmadi" in resp_json.get('error', '').lower():
                 print(f"Error Message Check: PASSED (Got readable error: {resp_json['error']})")
            else:
                 print(f"Error Message Check: WARN (Got: {resp_json['error']})")
        else:
            print("Check FAILED: Expected failure but got success.")
            print(resp_json)
    except:
        print("Check FAILED: Invalid JSON response")

if __name__ == "__main__":
    test_error_handling()
