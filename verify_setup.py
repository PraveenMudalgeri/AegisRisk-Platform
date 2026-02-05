import requests
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    try:
        r = requests.get(f"{BASE_URL}/")
        assert r.status_code == 200
        print("✅ Health check passed")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)

def test_auth_flow():
    # 1. Register
    email = "admin@aegisrisk.com"
    password = "securepassword123"
    org_name = "Acme Corp"
    
    # Clean up potentially existing user/org for idempotency could be hard without direct DB access, 
    # so we'll just try to login first.
    
    print("\nAttempting Login first...")
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if r.status_code == 200:
        print("User exists, logging in.")
        tokens = r.json()
    else:
        print("User not found, registering...")
        payload = {
            "email": email,
            "password": password,
            "organization_name": org_name,
            "industry": "Finance",
            "role": "ORG_ADMIN"
        }
        r = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if r.status_code != 200:
            print(f"❌ Registration failed: {r.text}")
            sys.exit(1)
        print("✅ Registration passed")
        
        # Login
        r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if r.status_code != 200:
             print(f"❌ Login after registration failed: {r.text}")
             sys.exit(1)
        tokens = r.json()

    print("✅ Login passed")
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # 2. Get Me (Protected)
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if r.status_code != 200:
         print(f"❌ Get Me failed: {r.text}")
         sys.exit(1)
    user_data = r.json()
    assert user_data["email"] == email
    print("✅ Protected Route (/auth/me) passed")

    # 3. Refresh Token
    r = requests.post(f"{BASE_URL}/auth/refresh", json={"refresh_token": refresh_token})
    if r.status_code != 200:
        print(f"❌ Refresh Token failed: {r.text}")
        sys.exit(1)
    new_tokens = r.json()
    assert "access_token" in new_tokens
    print("✅ Token Refresh passed")

    # 4. Logout
    r = requests.post(f"{BASE_URL}/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    if r.status_code != 200:
        print(f"❌ Logout failed: {r.text}")
        sys.exit(1)
    print("✅ Logout passed")

if __name__ == "__main__":
    test_health()
    test_auth_flow()
