from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..auth.jwt import get_current_user
from ..auth.models import User
from ..models import database as models
from ..models import schemas as schemas
from ..models.enums import Framework

router = APIRouter(
    prefix="/frameworks",
    tags=["frameworks"]
)

@router.get("/{framework}/controls", response_model=List[schemas.FrameworkControl])
def read_framework_controls(framework: Framework, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Everyone can read frameworks, but we require auth
    controls = db.query(models.FrameworkControl).filter(models.FrameworkControl.framework == framework).all()
    return controls
