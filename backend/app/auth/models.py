from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    industry = Column(String)

    users = relationship("User", back_populates="organization")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    role = Column(String) # "ORG_ADMIN", "RISK_ANALYST", "AUDITOR", "READ_ONLY"
    is_active = Column(Boolean, default=True)

    organization = relationship("Organization", back_populates="users")
