from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SqEnum, Float, DateTime, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
import datetime
from ..database import Base
from .enums import RiskSeverity, AssetType, STRIDECategory, ImplementationStatus, Framework, RiskLikelihood

# Note: Relationships to Organization and User are defined, but back_populates 
# will require updating the Auth models if bidirectional navigation is needed.
# For now, we assume one-way navigation or explicit joins for simple CRUD.

class Asset(Base):
    __tablename__ = "assets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    asset_type = Column(SqEnum(AssetType), nullable=False)
    criticality_score = Column(Integer, default=50) # 0-100
    owner_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # We deliberately don't set up back_populates on Organization/User to avoid cyclic imports 
    # and modifying auth module excessively for this step.
    # organization = relationship("Organization") 
    # owner = relationship("User") 
    
    threats = relationship("Threat", back_populates="asset", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="asset", cascade="all, delete-orphan")

class Threat(Base):
    __tablename__ = "threats"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    stride_category = Column(SqEnum(STRIDECategory), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    likelihood = Column(Float)
    impact = Column(Float)
    frequency_estimate = Column(String)

    asset = relationship("Asset", back_populates="threats")

class Control(Base):
    __tablename__ = "controls"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    implementation_status = Column(SqEnum(ImplementationStatus), default=ImplementationStatus.NOT_IMPLEMENTED)
    implementation_score = Column(Float, default=0.0) # 0-1
    evidence = Column(ARRAY(String), default=[])

class FrameworkControl(Base):
    __tablename__ = "framework_controls"
    id = Column(String, primary_key=True) # e.g. "ISO27001-A.5.1"
    framework = Column(SqEnum(Framework), nullable=False)
    control_id = Column(String, nullable=False) # e.g. "A.5.1"
    family = Column(String) # or Annex
    title = Column(String, nullable=False)
    description = Column(String)

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    assessment_date = Column(DateTime, default=datetime.datetime.utcnow)
    overall_score = Column(Float, default=0.0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    risks = Column(JSONB, default=[])

    asset = relationship("Asset", back_populates="risk_assessments")

class Risk(Base):
    __tablename__ = "risks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    threat_id = Column(UUID(as_uuid=True), ForeignKey("threats.id"))
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"))
    likelihood = Column(SqEnum(RiskLikelihood))
    severity = Column(SqEnum(RiskSeverity))
    risk_score = Column(Integer)
    status = Column(String) # Active, Mitigated, Accepted
    
    asset = relationship("Asset")
    threat = relationship("Threat")
