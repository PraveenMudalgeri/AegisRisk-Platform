from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.auth.models import User
from app.models.database import Asset, Threat
from app.models.enums import AssetType, STRIDECategory
import uuid

# Re-init DB tables to be safe (in a real test env we'd use a test db)
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

client = TestClient(app)

def verify_step3():
    print("Starting Step 3 Verification...")
    
    # 1. Register/Login
    unique_email = f"risk_admin_{uuid.uuid4().hex[:6]}@example.com"
    pwd = "securepassword"
    
    # Register
    reg_payload = {
        "email": unique_email,
        "password": pwd,
        "organization_name": "Risk Corp",
        "industry": "Finance",
        "role": "ORG_ADMIN"
    }
    client.post("/auth/register", json=reg_payload)
    
    # Login
    login_res = client.post("/auth/login", json={"email": unique_email, "password": pwd})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Authenticated as {unique_email}")
    
    # 2. Create Asset
    asset_payload = {
        "name": "Customer Database",
        "asset_type": "Data",
        "criticality_score": 90
    }
    asset_res = client.post("/api/assets/", json=asset_payload, headers=headers)
    assert asset_res.status_code == 200, f"Create asset failed: {asset_res.text}"
    asset_id = asset_res.json()["id"]
    print(f"Created Asset: {asset_id}")
    
    # 3. Enumerate Threats
    enum_res = client.post(f"/api/risks/threats/enumerate/{asset_id}", headers=headers)
    assert enum_res.status_code == 200
    threats = enum_res.json()
    assert len(threats) > 0
    print(f"Enumerated {len(threats)} potential threats.")
    
    # Verify we got some Data-related threats
    has_tampering = any(t["category"] == "Tampering" for t in threats)
    assert has_tampering, "Expected Tampering threats for Data asset"
    
    # 4. Create actual threats from suggestions
    # We need to add them to the DB effectively to assess them
    for t in threats[:3]: # Add first 3
        threat_payload = {
            "asset_id": asset_id,
            "stride_category": t["category"],
            "title": t["title"],
            "description": t["description"],
            "likelihood": 0.7,
            "impact": 0.8
        }
        client.post("/api/threats/", json=threat_payload, headers=headers)
    print("Added 3 active threats to asset.")
        
    # 5. Run Risk Assessment
    assess_res = client.post(f"/api/risks/assess/{asset_id}", headers=headers)
    assert assess_res.status_code == 200, f"Assessment failed: {assess_res.text}"
    assessment = assess_res.json()
    print(f"Risk Assessment Result: Score={assessment['overall_score']}")
    
    # 6. Check Dashboard
    dash_res = client.get("/api/risks/dashboard", headers=headers)
    assert dash_res.status_code == 200
    stats = dash_res.json()
    print("Dashboard Stats:", stats)
    assert stats["total_assessments"] >= 1
    
    print("Step 3 Verification Successful!")

if __name__ == "__main__":
    verify_step3()
