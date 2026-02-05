from ..models.enums import RiskSeverity

def calculate_ale(likelihood: float, impact: float) -> float:
    """
    Calculate Annual Loss Expectancy (ALE).
    ALE = Single Loss Expectancy (SLE) * Annualized Rate of Occurrence (ARO)
    Here we simplify: likelihood (frequency/prob) * impact (cost/loss)
    """
    return likelihood * impact

def get_risk_severity(risk_score: float) -> RiskSeverity:
    if risk_score >= 80:
        return RiskSeverity.CRITICAL
    elif risk_score >= 60:
        return RiskSeverity.HIGH
    elif risk_score >= 40:
        return RiskSeverity.MEDIUM
    elif risk_score >= 20:
        return RiskSeverity.LOW
    else:
        return RiskSeverity.INFORMATIONAL
