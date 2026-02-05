import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import database as models
from app.auth.models import User
from app.models.enums import AssetType, RiskSeverity, RiskLikelihood, ImplementationStatus, Framework

def seed_data():
    db = SessionLocal()
    try:
        print("Seeding Production Data...")
        
        # 1. Assets
        assets_data = [
            {"name": "Customer Portal DB", "type": AssetType.DATA, "score": 90, "desc": "Main Postgres database storing PII"},
            {"name": "Payment Gateway API", "type": AssetType.SOFTWARE, "score": 95, "desc": "Internal proxy to Stripe"},
            {"name": "Developer Laptops", "type": AssetType.HARDWARE, "score": 60, "desc": "Fleet of MacBook Pros"},
            {"name": "Corporate Website", "type": AssetType.SOFTWARE, "score": 40, "desc": "Public marketing site"},
            {"name": "Employee Directory", "type": AssetType.PEOPLE, "score": 50, "desc": "HR Information System"}
        ]
        
        assets = []
        for a in assets_data:
            asset = models.Asset(
                name=a["name"],
                description=a["desc"],
                asset_type=a["type"],
                criticality_score=a["score"],
                org_id="default-org"
            )
            db.add(asset)
            assets.append(asset)
        
        db.commit()
        for a in assets: db.refresh(a)
        print(f"Created {len(assets)} Assets")

        # 2. Controls
        controls_data = [
             {"name": "MFA for All Users", "status": ImplementationStatus.IMPLEMENTED, "score": 100},
             {"name": "Database Encryption at Rest", "status": ImplementationStatus.IMPLEMENTED, "score": 100},
             {"name": "Regular Phishing Tests", "status": ImplementationStatus.PARTIAL, "score": 50},
             {"name": "SOC 2 Audit", "status": ImplementationStatus.PLANNED, "score": 0},
             {"name": "Static Code Analysis (SAST)", "status": ImplementationStatus.IMPLEMENTED, "score": 90},
             {"name": "Container Scanning", "status": ImplementationStatus.PARTIAL, "score": 60},
             {"name": "Incident Response Plan", "status": ImplementationStatus.IMPLEMENTED, "score": 100},
             {"name": "Vendor Risk Assessment", "status": ImplementationStatus.PLANNED, "score": 0},
             {"name": "Access Review Quarterly", "status": ImplementationStatus.PARTIAL, "score": 75},
             {"name": "Log Aggregation (SIEM)", "status": ImplementationStatus.IMPLEMENTED, "score": 85}
        ]

        for c in controls_data:
            control = models.Control(
                name=c["name"],
                description=f"Control to mitigate risks related to {c['name']}",
                control_type="Preventive",
                frameworks=[Framework.NIST, Framework.ISO27001],
                implementation_status=c["status"],
                implementation_score=c["score"]
            )
            db.add(control)
        
        db.commit()
        print(f"Created {len(controls_data)} Controls")

        # 3. Threats & Risks
        threat_titles = [
            "SQL Injection", "Cross-Site Scripting", "Broken Authentication", "Sensitive Data Exposure",
            "XML External Entities", "Broken Access Control", "Security Misconfiguration", "Insecure Deserialization",
            "Using Components with Known Vulnerabilities", "Insufficient Logging"
        ]

        count = 0
        for asset in assets:
            # Add 2-3 threats per asset
            num_threats = random.randint(2, 4)
            for _ in range(num_threats):
                title = random.choice(threat_titles)
                threat = models.Threat(
                    title=f"{title} on {asset.name}",
                    description="Standard OWASP Top 10 threat vector",
                    asset_id=asset.id,
                    stride_category=random.choice(list(models.STRIDECategory)),
                    status="Open"
                )
                db.add(threat)
                db.commit()
                db.refresh(threat)
                
                # Create Risk for threat
                risk = models.Risk(
                    title=threat.title,
                    description=threat.description,
                    threat_id=threat.id,
                    asset_id=asset.id,
                    likelihood=random.choice(list(RiskLikelihood)),
                    severity=random.choice(list(RiskSeverity)),
                    risk_score=random.randint(10, 100),
                    status="Active"
                )
                db.add(risk)
                count += 1
        
        db.commit()
        print(f"Created {count} Threats & Risks")
        
        print("Data Seeding Complete!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
