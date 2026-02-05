from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database import get_db
from ..auth.jwt import get_current_user
from ..auth.models import User
from ..services.report_generator import ReportGenerator

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

@router.post("/generate", response_model=Dict[str, Any])
def generate_report(
    report_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a system report.
    report_type: 'risk_summary' | 'compliance'
    """
    generator = ReportGenerator(db)
    
    if report_type == 'risk_summary':
        return generator.generate_risk_summary()
    elif report_type == 'compliance':
        return generator.generate_compliance_report()
    else:
        raise HTTPException(status_code=400, detail="Invalid report type. Use 'risk_summary' or 'compliance'.")
