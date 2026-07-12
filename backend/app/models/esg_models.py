from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="employee")
    department = Column(String(100), nullable=True)
    points = Column(Integer, nullable=True, default=0)
    xp = Column(Integer, nullable=True, default=0)

    carbon_logs = relationship("CarbonLog", back_populates="user")
    carbon_transactions = relationship("CarbonTransaction", back_populates="user")
    csr_activity_records = relationship("CSRActivityRecord", back_populates="user")
    csr_participations = relationship("CSRParticipation", back_populates="user")
    policy_acknowledgements = relationship("PolicyAcknowledgement", back_populates="user")
    governance_audits = relationship("GovernanceAudit", back_populates="user")
    compliance_issues = relationship("ComplianceIssue", back_populates="user")
    challenges = relationship("Challenge", back_populates="user")
    challenge_participations = relationship("ChallengeParticipation", back_populates="user")
    reward_redemptions = relationship("RewardRedemption", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class CarbonLog(Base):
    __tablename__ = "carbon_logs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    date = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="carbon_logs")


class CarbonTransaction(Base):
    __tablename__ = "carbon_transactions"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    activity_quantity = Column(Float, nullable=False)
    emission_factor = Column(Float, nullable=False)
    emission_value = Column(Float, nullable=False)
    transaction_date = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="carbon_transactions")


class CSRActivity(Base):
    __tablename__ = "csr_activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(100), nullable=False)
    organizer = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="csr_activities")


class CSRActivityRecord(Base):
    __tablename__ = "csr_activity_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(80), nullable=False, default="Community and Environment")
    department = Column(String(80), nullable=False, default="Operations")
    location = Column(String(100), nullable=False)
    organizer = Column(String(100), nullable=False)
    start_date = Column(String(30), nullable=True)
    end_date = Column(String(30), nullable=True)
    max_participants = Column(Integer, nullable=True)
    points = Column(Integer, nullable=True, default=100)
    evidence_required = Column(Boolean, nullable=True, default=False)
    status = Column(String(30), nullable=False, default="Active")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="csr_activity_records")
    participations = relationship("CSRParticipation", back_populates="activity")


class CSRParticipation(Base):
    __tablename__ = "csr_participations"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("csr_activity_records.id"), nullable=False)
    employee = Column(String(100), nullable=False)
    proof_attachment = Column(String(255), nullable=True)
    approval_status = Column(String(30), nullable=False, default="Submitted")
    points_earned = Column(Integer, nullable=True, default=0)
    completion_date = Column(String(30), nullable=True)
    approval_remarks = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    activity = relationship("CSRActivityRecord", back_populates="participations")
    user = relationship("User", back_populates="csr_participations")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String(20), nullable=False)
    status = Column(String(30), nullable=False, default="draft")


class PolicyAcknowledgement(Base):
    __tablename__ = "policy_acknowledgements"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledgement_status = Column(String(20), nullable=False, default="Pending")
    acknowledgement_date = Column(String(30), nullable=True)
    reminder_status = Column(String(20), nullable=False, default="Pending")

    user = relationship("User", back_populates="policy_acknowledgements")


class GovernanceAudit(Base):
    __tablename__ = "governance_audits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    department = Column(String(100), nullable=False)
    auditor = Column(String(100), nullable=False)
    start_date = Column(String(30), nullable=True)
    end_date = Column(String(30), nullable=True)
    status = Column(String(30), nullable=False, default="Draft")
    findings = Column(Text, nullable=True)
    governance_score = Column(Integer, nullable=True, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="governance_audits")


class ComplianceIssue(Base):
    __tablename__ = "compliance_issues"

    id = Column(Integer, primary_key=True, index=True)
    related_audit_id = Column(Integer, nullable=True)
    severity = Column(String(30), nullable=False, default="Medium")
    description = Column(Text, nullable=False)
    assigned_owner = Column(String(100), nullable=False)
    due_date = Column(String(30), nullable=False)
    status = Column(String(30), nullable=False, default="Open")
    resolution_notes = Column(Text, nullable=True)
    overdue_flag = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="compliance_issues")


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    category = Column(String(80), nullable=False, default="Sustainability")
    description = Column(Text, nullable=True)
    xp_reward = Column(Integer, nullable=False, default=150)
    difficulty = Column(String(30), nullable=False, default="Medium")
    evidence_required = Column(Boolean, nullable=False, default=True)
    deadline = Column(String(30), nullable=True)
    status = Column(String(30), nullable=False, default="Active")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="challenges")
    participations = relationship("ChallengeParticipation", back_populates="challenge")


class ChallengeParticipation(Base):
    __tablename__ = "challenge_participations"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    employee = Column(String(100), nullable=False)
    progress = Column(String(50), nullable=False, default="0%")
    proof_attachment = Column(String(255), nullable=True)
    approval_status = Column(String(30), nullable=False, default="Submitted")
    xp_awarded = Column(Integer, nullable=True, default=0)
    completion_date = Column(String(30), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    challenge = relationship("Challenge", back_populates="participations")
    user = relationship("User", back_populates="challenge_participations")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    unlock_metric = Column(String(50), nullable=False, default="xp")
    unlock_value = Column(Integer, nullable=False, default=500)
    status = Column(String(30), nullable=False, default="Active")


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    points_required = Column(Integer, nullable=False, default=300)
    stock = Column(Integer, nullable=False, default=20)
    status = Column(String(30), nullable=False, default="Active")


class RewardRedemption(Base):
    __tablename__ = "reward_redemptions"

    id = Column(Integer, primary_key=True, index=True)
    reward_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    points_used = Column(Integer, nullable=False, default=0)
    status = Column(String(30), nullable=False, default="Redeemed")
    redeemed_at = Column(String(30), nullable=True)

    user = relationship("User", back_populates="reward_redemptions")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="notifications")
