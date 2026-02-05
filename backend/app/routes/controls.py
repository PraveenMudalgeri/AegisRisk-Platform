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
    prefix="/controls",
    tags=["controls"]
)

@router.post("/", response_model=schemas.Control)
def create_control(control: schemas.ControlCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_control = models.Control(**control.model_dump(), org_id=current_user.organization_id)
    db.add(db_control)
    db.commit()
    db.refresh(db_control)
    return db_control

@router.get("/", response_model=List[schemas.Control])
def read_controls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    controls = db.query(models.Control).filter(models.Control.org_id == current_user.organization_id).offset(skip).limit(limit).all()
    return controls

@router.put("/{control_id}", response_model=schemas.Control)
def update_control(control_id: UUID, control_update: schemas.ControlUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_control = db.query(models.Control).filter(models.Control.id == control_id, models.Control.org_id == current_user.organization_id).first()
    if not db_control:
        raise HTTPException(status_code=404, detail="Control not found")
        
    update_data = control_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_control, key, value)
    
    db.commit()
    db.refresh(db_control)
    return db_control
