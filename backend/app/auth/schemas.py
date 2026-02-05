from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from uuid import UUID

class OrganizationBase(BaseModel):
    name: str
    industry: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: UUID

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    role: Literal["ORG_ADMIN", "RISK_ANALYST", "AUDITOR", "READ_ONLY"]

class UserCreate(UserBase):
    password: str
    organization_name: str
    industry: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    organization_id: UUID
    organization: Organization

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
