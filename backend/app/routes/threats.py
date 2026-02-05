from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..auth.jwt import get_current_user
from ..auth.models import User
from ..models import database as models
from ..models import schemas as schemas

router = APIRouter(
    prefix="/threats",
    tags=["threats"]
)

@router.post("/", response_model=schemas.Threat)
def create_threat(threat: schemas.ThreatCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify asset belongs to user's org
    asset = db.query(models.Asset).filter(models.Asset.id == threat.asset_id, models.Asset.org_id == current_user.organization_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    db_threat = models.Threat(**threat.model_dump())
    db.add(db_threat)
    db.commit()
    db.refresh(db_threat)
    return db_threat

@router.get("/", response_model=List[schemas.Threat])
def read_threats(asset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify asset belongs to user's org
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.org_id == current_user.organization_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    threats = db.query(models.Threat).filter(models.Threat.asset_id == asset_id).all()
    return threats
