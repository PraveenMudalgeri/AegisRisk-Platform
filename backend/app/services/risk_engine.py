from typing import Dict, List, Any
from .utils import calculate_ale, get_risk_severity
from ..models.enums import RiskSeverity

class RiskEngine:
    def calculate_risk_score(
        self, 
        asset_value: float, 
        threat_likelihood: float, 
        threat_impact: float, 
        control_efficacy: float
    ) -> Dict[str, Any]:
        """
        Calculate risk score using a simplified FAIR-like approach.
        
        Args:
            asset_value: 0-100 (criticality)
            threat_likelihood: 0.0-1.0 (frequency)
            threat_impact: 0.0-1.0 (magnitude)
            control_efficacy: 0.0-1.0 (vulnerability mitigation)
            
        Returns dict with score, severity, etc.
        """
        
        # 1. Inherent Risk
        # Likelihood * Impact * Asset Value
        # If threat impact is high and asset is critical, inherent risk is high.
        inherent_risk = threat_likelihood * threat_impact * asset_value
        
        # 2. Residual Risk
        # Inherent Risk * (1 - Control Efficacy)
        # E.g. 100 * (1 - 0.8) = 20
        residual_risk = inherent_risk * (1.0 - control_efficacy)
        
        # Normalize to 0-100 scale if it exceeds
        risk_score = min(100.0, max(0.0, residual_risk))
        
        severity = get_risk_severity(risk_score)
        
        # Annualized Loss Expectancy (ALE) estimation
        # Assuming asset_value maps to a monetary figure roughly
        # This is a very rough heuristic for the API
        monetary_value = asset_value * 1000 # E.g. 50 score -> $50k
        ale = calculate_ale(threat_likelihood, monetary_value * threat_impact)
        
        return {
            "risk_score": round(risk_score, 2),
            "severity": severity,
            "inherent_risk": round(inherent_risk, 2),
            "residual_risk": round(residual_risk, 2),
            "ale": round(ale, 2)
        }

risk_engine = RiskEngine()
