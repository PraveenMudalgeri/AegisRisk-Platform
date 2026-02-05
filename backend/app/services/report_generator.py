from sqlalchemy.orm import Session
from ..models import database as models
from ..models.enums import RiskSeverity, ImplementationStatus

class ReportGenerator:
    def __init__(self, db: Session):
        self.db = db

    def generate_risk_summary(self):
        assets = self.db.query(models.Asset).all()
        threats = self.db.query(models.Threat).all()
        risks = self.db.query(models.Risk).all()
        
        # Calculate totals
        total_assets = len(assets)
        total_threats = len(threats)
        total_risks = len(risks)
        
        # Risk Distribution
        severity_counts = {sev.value: 0 for sev in RiskSeverity}
        for risk in risks:
            if risk.severity:
                severity_counts[risk.severity.value] += 1
                
        # Top Critical Assets
        critical_assets = [
            {
                "name": a.name,
                "type": a.asset_type,
                "score": a.criticality_score
            }
            for a in sorted(assets, key=lambda x: x.criticality_score, reverse=True)[:5]
        ]

        return {
            "title": "Executive Risk Summary",
            "generated_at": "2026-02-05T12:00:00Z", # In real app, use datetime.utcnow
            "summary_stats": {
                "total_assets": total_assets,
                "total_threats": total_threats,
                "total_risks": total_risks,
            },
            "risk_severity_distribution": severity_counts,
            "top_critical_assets": critical_assets
        }

    def generate_compliance_report(self):
        controls = self.db.query(models.Control).all()
        
        total_controls = len(controls)
        implemented = sum(1 for c in controls if c.implementation_status == ImplementationStatus.IMPLEMENTED)
        planned = sum(1 for c in controls if c.implementation_status == ImplementationStatus.PLANNED)
        missing = total_controls - implemented - planned
        
        # Mock Framework Coverage (since we don't have full mapping in DB yet)
        framework_coverage = {
            "ISO 27001": {"score": 65, "status": "Partial"},
            "NIST 800-53": {"score": 48, "status": "At Risk"},
            "GDPR": {"score": 80, "status": "Good"}
        }

        return {
            "title": "Compliance & Control Status",
            "generated_at": "2026-02-05T12:00:00Z",
            "control_stats": {
                "total": total_controls,
                "implemented": implemented,
                "planned": planned,
                "missing": missing,
                "implementation_percentage": round((implemented / total_controls * 100) if total_controls else 0, 1)
            },
            "framework_coverage": framework_coverage
        }
