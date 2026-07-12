from typing import List
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


class CarbonTransactionRequest(BaseModel):
    source: str
    activity_quantity: float
    emission_factor: float
    transaction_date: str
    description: str | None = None


class CSRActivityRequest(BaseModel):
    title: str
    description: str
    location: str
    organizer: str


class CSRActivityDetailRequest(BaseModel):
    title: str
    description: str
    category: str = "Community and Environment"
    department: str = "Operations"
    location: str
    organizer: str
    start_date: str | None = None
    end_date: str | None = None
    max_participants: int | None = None
    points: int = 100
    evidence_required: bool = False
    status: str = "Active"


class CSRParticipationRequest(BaseModel):
    activity_id: int
    employee: str
    proof_attachment: str | None = None
    approval_status: str = "Submitted"
    points_earned: int = 0
    completion_date: str | None = None
    approval_remarks: str | None = None


class GovernancePolicyRequest(BaseModel):
    title: str
    description: str
    version: str
    status: str = "draft"


class GovernanceAuditRequest(BaseModel):
    title: str
    department: str
    auditor: str
    start_date: str | None = None
    end_date: str | None = None
    status: str = "Draft"
    findings: str | None = None
    governance_score: int = 0


class ComplianceIssueRequest(BaseModel):
    related_audit_id: int | None = None
    severity: str = "Medium"
    description: str
    assigned_owner: str
    due_date: str
    status: str = "Open"
    resolution_notes: str | None = None


class ChallengeRequest(BaseModel):
    title: str
    category: str = "Sustainability"
    description: str | None = None
    xp_reward: int = 150
    difficulty: str = "Medium"
    evidence_required: bool = True
    deadline: str | None = None
    status: str = "Active"


class ChallengeParticipationRequest(BaseModel):
    challenge_id: int
    employee: str
    progress: str = "0%"
    proof_attachment: str | None = None
    approval_status: str = "Submitted"
    xp_awarded: int = 0
    completion_date: str | None = None


class BadgeRequest(BaseModel):
    name: str
    description: str | None = None
    icon: str | None = None
    unlock_metric: str = "xp"
    unlock_value: int = 500
    status: str = "Active"


class RewardRequest(BaseModel):
    name: str
    description: str | None = None
    points_required: int = 300
    stock: int = 20
    status: str = "Active"


class RewardRedemptionRequest(BaseModel):
    reward_id: int
    points_used: int = 0


class ReportResponse(BaseModel):
    report_id: str
    title: str
    summary: str
    recommendations: List[str]


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
