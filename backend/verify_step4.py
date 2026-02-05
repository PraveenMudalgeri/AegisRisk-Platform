import httpx
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def verify_step4():
    print("Starting Step 4 Verification...")
    
    # 1. Login
    unique_email = f"compliance_officer_{uuid4().hex[:6]}@example.com"
    pwd = "securepassword"
    
    client.post("/auth/register", json={
        "email": unique_email, 
        "password": pwd,
        "organization_name": "Mapped Corp",
        "industry": "Tech",
        "role": "ORG_ADMIN"
    })
    
    login_res = client.post("/auth/login", json={"email": unique_email, "password": pwd})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Authenticated.")
    
    # 2. Check Assessment (Should be 0% initially)
    assess_res = client.post("/api/mappings/assess", headers=headers)
    assert assess_res.status_code == 200
    stats = assess_res.json()
    print("Initial Stats:", stats)
    assert stats["ISO 27001"]["percentage"] == 0
    
    # 3. Implement a Control (ISO 27001-A.9.2.1)
    # First create it in Org context
    ctrl_payload = {
        "name": "ISO27001-A.9.2.1",
        "description": "User Reg",
        "implementation_status": "Implemented", # Case sensitive per Enum?
        "implementation_score": 1.0
    }
    # Note: Check Enum value in backend. It's "Implemented".
    
    create_res = client.post("/api/controls/", json=ctrl_payload, headers=headers)
    if create_res.status_code != 200:
        print("Create Control Failed:", create_res.text)
        exit(1)
        
    control_id = create_res.json()["id"]
    print(f"Implemented control {control_id}")
    
    # 4. Check Assessment Again
    assess_res_2 = client.post("/api/mappings/assess", headers=headers)
    stats_2 = assess_res_2.json()
    print("Updated Stats:", stats_2["ISO 27001"])
    assert stats_2["ISO 27001"]["covered"] >= 1
    
    # 5. Check Mapping Endpoint
    map_res = client.get("/api/mappings/ISO27001-A.9.2.1", headers=headers)
    assert map_res.status_code == 200
    mapping_data = map_res.json()
    print("Mapping Data:", mapping_data)
    assert "NIST-AC-2" in mapping_data["mappings"]["NIST 800-53"]
    
    # 6. Attach Evidence
    evidence_payload = {"evidence_url": "http://sharepoint/policy.pdf"}
    # Note: API expects query param? Let's check route signature.
    # Route: def attach_evidence(control_id: UUID, evidence_url: str ...
    # It's a query param by default in FastAPI if not Path/Body.
    
    ev_res = client.post(f"/api/mappings/{control_id}/evidence?evidence_url=http://example.com/doc", headers=headers)
    assert ev_res.status_code == 200
    print("Evidence attached:", ev_res.json())
    
    print("Step 4 Verification Successful!")

if __name__ == "__main__":
    verify_step4()
