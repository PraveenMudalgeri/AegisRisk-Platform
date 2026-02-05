import json
import os
import sys

# Add the directory containing the app module to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.database import SessionLocal
from app.models.database import FrameworkControl
from app.models.enums import Framework

def seed_data():
    db = SessionLocal()
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    iso_path = os.path.join(base_dir, "iso27001_controls.json")
    nist_path = os.path.join(base_dir, "nist_800_53_controls.json")
    
    print("Seeding Framework Controls...")
    
    # Load ISO
    try:
        with open(iso_path, "r") as f:
            iso_data = json.load(f)
            for item in iso_data:
                exists = db.query(FrameworkControl).filter_by(id=item["id"]).first()
                if not exists:
                    ctrl = FrameworkControl(
                        id=item["id"],
                        framework=Framework(item["framework"]),
                        control_id=item["control_id"],
                        family=item["family"],
                        title=item["title"],
                        description=item["description"]
                    )
                    db.add(ctrl)
            print(f"Processed {len(iso_data)} ISO 27001 controls.")
    except Exception as e:
        print(f"Error loading ISO 27001 data: {e}")
    
    # Load NIST
    try:
        with open(nist_path, "r") as f:
            nist_data = json.load(f)
            for item in nist_data:
                exists = db.query(FrameworkControl).filter_by(id=item["id"]).first()
                if not exists:
                    ctrl = FrameworkControl(
                        id=item["id"],
                        framework=Framework(item["framework"]),
                        control_id=item["control_id"],
                        family=item["family"],
                        title=item["title"],
                        description=item["description"]
                    )
                    db.add(ctrl)
            print(f"Processed {len(nist_data)} NIST 800-53 controls.")
    except Exception as e:
        print(f"Error loading NIST 800-53 data: {e}")
    
    db.commit()
    db.close()
    print("Seed data loaded successfully.")

if __name__ == "__main__":
    seed_data()
