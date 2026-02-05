from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
from .enums import RiskSeverity, AssetType, STRIDECategory, ImplementationStatus, Framework

# -- Asset Schemas --

class AssetBase(BaseModel):
    name: str
    description: Optional[str] = None
    asset_type: AssetType
    criticality_score: int = 50
    tags: List[str] = []

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    asset_type: Optional[AssetType] = None
    criticality_score: Optional[int] = None
    tags: Optional[List[str]] = None

class Asset(AssetBase):
    id: UUID
    org_id: UUID
    owner_id: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# -- Threat Schemas --

class ThreatBase(BaseModel):
    stride_category: STRIDECategory
    title: str
    description: Optional[str] = None
    likelihood: Optional[float] = None
    impact: Optional[float] = None
    frequency_estimate: Optional[str] = None

class ThreatCreate(ThreatBase):
    asset_id: UUID
    pass

    
class Threat(ThreatBase):
    id: UUID
    asset_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# -- Control Schemas --

class ControlBase(BaseModel):
    name: str
    description: Optional[str] = None
    implementation_status: ImplementationStatus = ImplementationStatus.NOT_IMPLEMENTED
    implementation_score: float = 0.0
    evidence: List[str] = []

class ControlCreate(ControlBase):
    pass

class ControlUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    implementation_status: Optional[ImplementationStatus] = None
    implementation_score: Optional[float] = None
    evidence: Optional[List[str]] = None

class Control(ControlBase):
    id: UUID
    org_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

# -- Framework Control Schemas --

class FrameworkControl(BaseModel):
    id: str
    framework: Framework
    control_id: str
    family: Optional[str] = None
    title: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# -- RiskAssessment Schemas --

class RiskAssessmentBase(BaseModel):
    overall_score: float = 0.0
    critical_count: int = 0
    high_count: int = 0
    risks: Any = [] # List[Dict] usually

class RiskAssessmentCreate(RiskAssessmentBase):
    asset_id: UUID

class RiskAssessment(RiskAssessmentBase):
    id: UUID
    asset_id: UUID
    assessment_date: datetime
    
    model_config = ConfigDict(from_attributes=True)
