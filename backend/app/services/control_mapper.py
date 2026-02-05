import json
import os
from typing import List, Dict, Any, Set
from sqlalchemy.orm import Session
from uuid import UUID

from ..models import database as models
from ..models.enums import Framework, ImplementationStatus

class ControlMapper:
    def __init__(self):
        self.mappings = self._load_mappings()

    def _load_mappings(self) -> Dict[str, List[str]]:
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "data", "cross_framework_mappings.json")
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading mappings: {e}")
            return {}

    def map_control_to_frameworks(self, control_id: str) -> Dict[str, List[str]]:
        """
        Given a control ID (e.g., ISO27001-A.5.1), return mapped controls in other frameworks.
        Currently supports ISO -> NIST mapping from JSON.
        """
        mappings = {"NIST 800-53": [], "ISO 27001": []}
        
        # Direct lookup (ISO -> NIST)
        if control_id in self.mappings:
            mappings["NIST 800-53"] = self.mappings[control_id]
            
        # Reverse lookup (NIST -> ISO) - inefficient but works for small dataset
        for iso_id, nist_ids in self.mappings.items():
            if control_id in nist_ids:
                mappings["ISO 27001"].append(iso_id)
                
        return mappings

    def assess_org_coverage(self, db: Session, org_id: UUID) -> Dict[str, Any]:
        """
        Calculate percentage coverage for each framework based on IMPLEMENTED controls.
        """
        # 1. Get all Framework Controls (The Denominator)
        # In a real app, we'd filter by what the Org cares about. 
        # Here we assume they care about all seeded FrameworkControls.
        all_fw_controls = db.query(models.FrameworkControl).all()
        
        framework_totals = {}
        for fc in all_fw_controls:
            fw = fc.framework.value
            framework_totals[fw] = framework_totals.get(fw, 0) + 1
            
        # 2. Get Org's Implemented Controls (The Numerator)
        # We need to match Org Controls to Framework Controls.
        # Currently, our "Control" model is generic. 
        # Ideally, "Control" should link to "FrameworkControl".
        # For this MVP, let's assume Org Controls *are* instances of Framework Controls
        # if their 'name' matches the framework control ID (e.g. "ISO27001-A.5.1").
        
        implemented_controls = db.query(models.Control).filter(
            models.Control.org_id == org_id,
            models.Control.implementation_status == ImplementationStatus.IMPLEMENTED
        ).all()
        
        # Track coverage
        coverage_counts = {fw: 0 for fw in framework_totals.keys()}
        covered_ids = {fw: set() for fw in framework_totals.keys()}
        
        for ic in implemented_controls:
            # Check if name is a known Framework Control ID
            # This is a loose coupling for MVP.
            fw_ctrl = db.query(models.FrameworkControl).filter(models.FrameworkControl.id == ic.name).first()
            if fw_ctrl:
                fw = fw_ctrl.framework.value
                if fw in coverage_counts and ic.name not in covered_ids[fw]:
                    coverage_counts[fw] += 1
                    covered_ids[fw].add(ic.name)
            
            # Also check mappings! existing valid control implies mapped control is covered?
            # Start simple: Direct coverage only.
            
        # Calculate percentages
        results = {}
        for fw, total in framework_totals.items():
            covered = coverage_counts.get(fw, 0)
            percentage = round((covered / total) * 100, 1) if total > 0 else 0
            results[fw] = {
                "covered": covered,
                "total": total,
                "percentage": percentage
            }
            
        return results

control_mapper = ControlMapper()
