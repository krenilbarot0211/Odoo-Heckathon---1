from typing import List, Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "employee"


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class CarbonLogRequest(BaseModel):
    source: str
    amount: float
    unit: str
    date: str


class CSRActivityRequest(BaseModel):
    title: str
    description: str
    location: str
    organizer: str


class GovernancePolicyRequest(BaseModel):
    title: str
    description: str
    version: str
    status: str = "draft"


class ReportResponse(BaseModel):
    report_id: str
    title: str
    summary: str
    recommendations: List[str]
