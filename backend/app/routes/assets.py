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
    prefix="/assets",
    tags=["assets"]
)

@router.post("/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_asset = models.Asset(**asset.model_dump(), org_id=current_user.organization_id, owner_id=current_user.id)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/", response_model=List[schemas.Asset])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Filter by user's organization
    assets = db.query(models.Asset).filter(models.Asset.org_id == current_user.organization_id).offset(skip).limit(limit).all()
    return assets

@router.get("/{asset_id}", response_model=schemas.Asset)
def read_asset(asset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.org_id == current_user.organization_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: UUID, asset_update: schemas.AssetUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.org_id == current_user.organization_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{asset_id}")
def delete_asset(asset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.org_id == current_user.organization_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db.delete(db_asset)
    db.commit()
    return {"ok": True}
