from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID

from ..database import get_db
from ..auth.jwt import get_current_user
from ..auth.models import User
from ..models import database as models
from ..models import schemas as schemas
from ..models.enums import RiskSeverity

from ..services.threat_engine import threat_engine
from ..services.risk_engine import risk_engine
from ..services.threat_control_mapper import threat_control_mapper

router = APIRouter(
    prefix="/risks",
    tags=["risks"]
)

@router.post("/threats/enumerate/{asset_id}")
def enumerate_threats(asset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.org_id == current_user.organization_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    potential_threats = threat_engine.enumerate_threats(asset.asset_type)
    
    # Enrich with controls
    for threat in potential_threats:
        threat["recommended_controls"] = threat_control_mapper.recommend_controls(threat["category"])
        
    return potential_threats

@router.post("/assess/{asset_id}", response_model=schemas.RiskAssessment)
def assess_risk(asset_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id, models.Asset.org_id == current_user.organization_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Get existing threats for this asset
    threats = db.query(models.Threat).filter(models.Threat.asset_id == asset_id).all()
    if not threats:
         raise HTTPException(status_code=400, detail="No threats found for asset. Please add threats first.")

    # Calculate risk for each threat
    results = []
    overall_score = 0.0
    critical_count = 0
    high_count = 0
    
    for threat in threats:
        # Simplified: assume 0.5 control efficacy if not linked to real controls yet
        # Future: Lookup controls linked to this threat or asset
        control_efficacy = 0.5 
        
        # Ensure we have float values. Defaults from model might need checking.
        likelihood = threat.likelihood if threat.likelihood else 0.5
        impact = threat.impact if threat.impact else 0.5
        
        calculation = risk_engine.calculate_risk_score(
            asset_value=float(asset.criticality_score),
            threat_likelihood=likelihood,
            threat_impact=impact,
            control_efficacy=control_efficacy
        )
        
        result_entry = {
            "threat_id": str(threat.id),
            "threat_title": threat.title,
            "calculation": calculation
        }
        results.append(result_entry)
        
        # Max risk score approach for overall asset risk? Or average?
        # Let's use Average for score, but counts for dashboard
        overall_score += calculation["risk_score"]
        
        if calculation["severity"] == RiskSeverity.CRITICAL:
            critical_count += 1
        elif calculation["severity"] == RiskSeverity.HIGH:
            high_count += 1
            
    if threats:
        overall_score /= len(threats)
    
    # Save Risk Assessment Record
    risk_assessment = models.RiskAssessment(
        asset_id=asset.id,
        overall_score=overall_score,
        critical_count=critical_count,
        high_count=high_count,
        risks=results
    )
    
    db.add(risk_assessment)
    db.commit()
    db.refresh(risk_assessment)
    
    return risk_assessment

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # This queries ALL user assets and their latest risk assessments
    # Optimized query would be better, but loop is fine for MVP
    
    start_q = db.query(models.RiskAssessment).join(models.Asset).filter(models.Asset.org_id == current_user.organization_id)
    assessments = start_q.all()
    
    stats = {
        "overall_score_avg": 0.0,
        "total_assessments": len(assessments),
        "severity_counts": {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0
        },
        "recent_assessments": []
    }
    
    if not assessments:
        return stats
        
    total_score = 0
    for ra in assessments:
        total_score += ra.overall_score
        stats["severity_counts"]["Critical"] += ra.critical_count
        stats["severity_counts"]["High"] += ra.high_count
        # Note: We only stored count of Crit/High in DB model. 
        # Ideally we'd calculate others from the JSON blob if needed.
        
        # Add basic info to recent list
        stats["recent_assessments"].append({
            "id": str(ra.id),
            "asset_id": str(ra.asset_id),
            "date": ra.assessment_date,
            "score": ra.overall_score
        })
        
    stats["overall_score_avg"] = round(total_score / len(assessments), 2)
    
    return stats

@router.get("/{assessment_id}", response_model=schemas.RiskAssessment)
def get_assessment(assessment_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ra = db.query(models.RiskAssessment).join(models.Asset).filter(
        models.RiskAssessment.id == assessment_id, 
        models.Asset.org_id == current_user.organization_id
    ).first()
    
    if not ra:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    return ra
