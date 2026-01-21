
import requests
import uuid

BASE_URL = "http://localhost:8010"  # Nginx port or 8000 depending on what's running. Let's try 8000 first as it's direct to backend if exposed, or 8010 if via Nginx.
# In previous context, we saw Nginx on 8010. 
# But usually local testing is on 8000 (uvicorn default). 
# Let's try 8000 first, if fails we can assume server isn't running or try 8010.
# Actually, the user might not have the server running. 
# I will assume the user needs to start the server. 
# But wait, I can try to run uvicorn in background? 
# No, I should assume the server might be running or I can run it briefly.
# Let's write the test assuming port 8000 (standard dev port).

URL = "http://localhost:8000"

def test_onboarding_flow():
    print("Testing Onboarding Flow...")
    
    # 1. Register a new user
    email = f"test_onboard_{uuid.uuid4().hex[:6]}@example.com"
    password = "password123"
    print(f"Registering user: {email}")
    
    response = requests.post(f"{URL}/auth/register", json={
        "email": email,
        "password": password
        # business_type is intentionally omitted to simulate Google Login (empty initially) 
        # or just a user who didn't select it yet.
        # Actually register endpoint allows business_type optional.
    })
    
    if response.status_code != 200:
        print(f"Registration failed: {response.text}")
        return

    data = response.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Registration successful.")

    # 2. Get User Info (GET /auth/me)
    print("Getting user info...")
    response = requests.get(f"{URL}/auth/me", headers=headers)
    if response.status_code != 200:
        print(f"GET /auth/me failed: {response.text}")
        return
    
    user_info = response.json()
    print(f"User Info: {user_info}")
    
    if user_info.get("business_type") is not None:
        print("Warning: business_type should be None initially for this test.")
    
    # 3. Update Business Type (PATCH /auth/me)
    print("Updating business type...")
    new_type = "oquv_markazi"
    response = requests.patch(f"{URL}/auth/me", json={"business_type": new_type}, headers=headers)
    
    if response.status_code != 200:
        print(f"PATCH /auth/me failed: {response.text}")
        return
        
    updated_info = response.json()
    print(f"Updated Info: {updated_info}")
    
    if updated_info.get("business_type") == new_type:
        print("SUCCESS: Business type updated correctly!")
    else:
        print("FAILURE: Business type did not update.")

if __name__ == "__main__":
    try:
        test_onboarding_flow()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure the server is running on http://localhost:8000")
