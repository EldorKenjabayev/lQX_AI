
import requests
import json

BASE_URL = "http://localhost:8000"
EMAIL = "test_chat_new@lqxai.com"
PASSWORD = "strongpassword123"

def test_chat():
    print("\n--- Testing Interactive Chatbot ---")
    
    # Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        # Register if needed
        requests.post(f"{BASE_URL}/auth/register", json={"email": EMAIL, "password": PASSWORD, "business_type": "O'quv Markazi"})
        resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
        
    if resp.status_code != 200:
        print(f"FATAL: Login failed. Status: {resp.status_code}, Response: {resp.text}")
        return

    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Upload Data (O'quv markazi)
    print("Uploading Edu Center Data...")
    try:
        with open("edu_center_2026.csv", 'rb') as f:
            files = {'file': ('edu_center_2026.csv', f, 'text/csv')}
            requests.post(f"{BASE_URL}/data/upload/csv", headers=headers, files=files)
    except:
        print("CSV not found, skipping upload (assuming already uploaded)")

    # 2. Ask Questions
    
    # Q1: General Advice
    print("\n[User]: O'quv markazim qalay? Risk bormi?")
    q1 = {"message": "O'quv markazim qalay? Risk bormi?", "initial_balance": 10000000}
    resp = requests.post(f"{BASE_URL}/chat/ask", headers=headers, json=q1)
    print(f"[AI]: {resp.json().get('response')}")
    
    # Q2: Expense Intent (Small)
    print("\n[User]: 5 mln so'mga yangi proyektor olsam bo'ladimi?")
    q2 = {"message": "5 mln so'mga yangi proyektor olsam bo'ladimi?", "initial_balance": 10000000}
    resp = requests.post(f"{BASE_URL}/chat/ask", headers=headers, json=q2)
    print(f"[AI]: {resp.json().get('response')}")
    
    # Q3: Expense Intent (Huge)
    print("\n[User]: 200 mln so'mga yangi mashina (Malibu) olsam bo'ladimi?")
    q3 = {"message": "200 mln so'mga yangi mashina (Malibu) olsam bo'ladimi?", "initial_balance": 10000000}
    resp = requests.post(f"{BASE_URL}/chat/ask", headers=headers, json=q3)
    data = resp.json()
    print(f"[AI]: {data.get('response')}")
    
    # Check Context
    context = data.get('context', {})
    if 'liquidity_check' in context:
        print(f"DEBUG Liquidity Check: {context['liquidity_check']}")
        
if __name__ == "__main__":
    test_chat()
