from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID

from ..database import get_db
from ..auth.jwt import get_current_user
from ..auth.models import User
from ..models import database as models
from ..models import schemas as schemas
from ..services.control_mapper import control_mapper

router = APIRouter(
    prefix="/mappings",
    tags=["mappings"]
)

@router.post("/assess")
def assess_coverage(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns framework coverage statistics for the user's organization.
    """
    stats = control_mapper.assess_org_coverage(db, current_user.organization_id)
    return stats

@router.get("/{control_id}")
def get_control_mappings(control_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get cross-framework mappings for a specific control ID (e.g. ISO27001-A.5.1).
    """
    # Verify the ID exists in our static data or DB? 
    # For now, just return what the mapper knows.
    mappings = control_mapper.map_control_to_frameworks(control_id)
    return {
        "control_id": control_id,
        "mappings": mappings
    }

@router.post("/{control_id}/evidence")
def attach_evidence(control_id: UUID, evidence_url: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Attach an evidence link to a specific *implemented* control.
    Note: control_id here is the UUID of the Control record, not the Framework ID.
    """
    control = db.query(models.Control).filter(
        models.Control.id == control_id,
        models.Control.org_id == current_user.organization_id
    ).first()
    
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
        
    # Append evidence
    if control.evidence is None:
        control.evidence = []
    
    # Create a new list to ensure mutation is tracked if using some ORM setups, 
    # though Postgres ARRAY usually updates fine.
    # Be safe:
    current_evidence = list(control.evidence)
    current_evidence.append(evidence_url)
    control.evidence = current_evidence
    
    db.commit()
    db.refresh(control)
    
    return {"status": "success", "evidence_count": len(control.evidence)}
