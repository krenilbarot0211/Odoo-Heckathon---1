from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.database import Base, engine
from app.models.esg_models import (
    Badge,
    CarbonLog,
    CarbonTransaction,
    Challenge,
    ChallengeParticipation,
    ComplianceIssue,
    CSRActivity,
    CSRActivityRecord,
    CSRParticipation,
    GovernanceAudit,
    Notification,
    Policy,
    PolicyAcknowledgement,
    Reward,
    RewardRedemption,
    User,
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

Base.metadata.create_all(bind=engine)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, name: str, email: str, password: str, role: str, department: str | None = None) -> User:
    user = User(
        name=name,
        email=email,
        password_hash=get_password_hash(password),
        role=role,
        department=department,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def add_carbon_log(db: Session, source: str, amount: float, unit: str, date: str, user_id: int | None = None) -> CarbonLog:
    log = CarbonLog(source=source, amount=amount, unit=unit, date=date, user_id=user_id)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def add_carbon_transaction(
    db: Session,
    source: str,
    activity_quantity: float,
    emission_factor: float,
    transaction_date: str,
    description: str | None = None,
    user_id: int | None = None,
) -> CarbonTransaction:
    emission_value = round(activity_quantity * emission_factor, 2)
    transaction = CarbonTransaction(
        source=source,
        activity_quantity=activity_quantity,
        emission_factor=emission_factor,
        emission_value=emission_value,
        transaction_date=transaction_date,
        description=description,
        user_id=user_id,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def list_carbon_logs(db: Session) -> list[CarbonLog]:
    return db.query(CarbonLog).all()


def list_carbon_transactions(db: Session) -> list[CarbonTransaction]:
    return db.query(CarbonTransaction).all()


def add_csr_activity(db: Session, title: str, description: str, location: str, organizer: str, user_id: int | None = None) -> CSRActivity:
    activity = CSRActivity(title=title, description=description, location=location, organizer=organizer, user_id=user_id)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def add_csr_activity_record(
    db: Session,
    title: str,
    description: str,
    category: str,
    department: str,
    location: str,
    organizer: str,
    start_date: str | None,
    end_date: str | None,
    max_participants: int | None,
    points: int,
    evidence_required: bool,
    status: str,
    user_id: int | None = None,
) -> CSRActivityRecord:
    record = CSRActivityRecord(
        title=title,
        description=description,
        category=category,
        department=department,
        location=location,
        organizer=organizer,
        start_date=start_date,
        end_date=end_date,
        max_participants=max_participants,
        points=points,
        evidence_required=evidence_required,
        status=status,
        user_id=user_id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def add_csr_participation(
    db: Session,
    activity_id: int,
    employee: str,
    proof_attachment: str | None,
    approval_status: str,
    points_earned: int,
    completion_date: str | None,
    approval_remarks: str | None,
    user_id: int | None = None,
) -> CSRParticipation:
    participation = CSRParticipation(
        activity_id=activity_id,
        employee=employee,
        proof_attachment=proof_attachment,
        approval_status=approval_status,
        points_earned=points_earned,
        completion_date=completion_date,
        approval_remarks=approval_remarks,
        user_id=user_id,
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation


def list_csr_activities(db: Session) -> list[CSRActivity]:
    return db.query(CSRActivity).all()


def list_csr_activity_records(db: Session) -> list[CSRActivityRecord]:
    return db.query(CSRActivityRecord).all()


def list_csr_participations(db: Session) -> list[CSRParticipation]:
    return db.query(CSRParticipation).all()


def add_policy(db: Session, title: str, description: str, version: str, status: str = "draft") -> Policy:
    policy = Policy(title=title, description=description, version=version, status=status)
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def add_policy_acknowledgement(
    db: Session,
    policy_id: int,
    user_id: int | None,
    acknowledgement_status: str,
    acknowledgement_date: str | None,
    reminder_status: str,
) -> PolicyAcknowledgement:
    record = PolicyAcknowledgement(
        policy_id=policy_id,
        user_id=user_id,
        acknowledgement_status=acknowledgement_status,
        acknowledgement_date=acknowledgement_date,
        reminder_status=reminder_status,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_policies(db: Session) -> list[Policy]:
    return db.query(Policy).all()


def add_governance_audit(
    db: Session,
    title: str,
    department: str,
    auditor: str,
    start_date: str | None,
    end_date: str | None,
    status: str,
    findings: str | None,
    governance_score: int,
    user_id: int | None = None,
) -> GovernanceAudit:
    audit = GovernanceAudit(
        title=title,
        department=department,
        auditor=auditor,
        start_date=start_date,
        end_date=end_date,
        status=status,
        findings=findings,
        governance_score=governance_score,
        user_id=user_id,
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


def add_compliance_issue(
    db: Session,
    related_audit_id: int | None,
    severity: str,
    description: str,
    assigned_owner: str,
    due_date: str,
    status: str,
    resolution_notes: str | None,
    overdue_flag: bool,
    user_id: int | None = None,
) -> ComplianceIssue:
    issue = ComplianceIssue(
        related_audit_id=related_audit_id,
        severity=severity,
        description=description,
        assigned_owner=assigned_owner,
        due_date=due_date,
        status=status,
        resolution_notes=resolution_notes,
        overdue_flag=overdue_flag,
        user_id=user_id,
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def list_compliance_issues(db: Session) -> list[ComplianceIssue]:
    return db.query(ComplianceIssue).all()


def add_challenge(
    db: Session,
    title: str,
    category: str,
    description: str | None,
    xp_reward: int,
    difficulty: str,
    evidence_required: bool,
    deadline: str | None,
    status: str,
    user_id: int | None = None,
) -> Challenge:
    challenge = Challenge(
        title=title,
        category=category,
        description=description,
        xp_reward=xp_reward,
        difficulty=difficulty,
        evidence_required=evidence_required,
        deadline=deadline,
        status=status,
        user_id=user_id,
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


def add_challenge_participation(
    db: Session,
    challenge_id: int,
    employee: str,
    progress: str,
    proof_attachment: str | None,
    approval_status: str,
    xp_awarded: int,
    completion_date: str | None,
    user_id: int | None = None,
) -> ChallengeParticipation:
    participation = ChallengeParticipation(
        challenge_id=challenge_id,
        employee=employee,
        progress=progress,
        proof_attachment=proof_attachment,
        approval_status=approval_status,
        xp_awarded=xp_awarded,
        completion_date=completion_date,
        user_id=user_id,
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation


def list_challenges(db: Session) -> list[Challenge]:
    return db.query(Challenge).all()


def add_badge(
    db: Session,
    name: str,
    description: str | None,
    icon: str | None,
    unlock_metric: str,
    unlock_value: int,
    status: str,
) -> Badge:
    badge = Badge(name=name, description=description, icon=icon, unlock_metric=unlock_metric, unlock_value=unlock_value, status=status)
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge


def list_badges(db: Session) -> list[Badge]:
    return db.query(Badge).all()


def add_reward(
    db: Session,
    name: str,
    description: str | None,
    points_required: int,
    stock: int,
    status: str,
) -> Reward:
    reward = Reward(name=name, description=description, points_required=points_required, stock=stock, status=status)
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


def list_rewards(db: Session) -> list[Reward]:
    return db.query(Reward).all()


def redeem_reward(db: Session, reward_id: int, user_id: int | None, points_used: int) -> RewardRedemption:
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward or reward.stock <= 0:
        raise ValueError("Reward unavailable")
    user = db.query(User).filter(User.id == user_id).first() if user_id is not None else None
    if user is None or (user.points or 0) < points_used:
        raise ValueError("Insufficient points")
    reward.stock -= 1
    user.points = (user.points or 0) - points_used
    redemption = RewardRedemption(reward_id=reward_id, user_id=user_id, points_used=points_used, redeemed_at=datetime.now(timezone.utc).isoformat())
    db.add(redemption)
    db.commit()
    db.refresh(redemption)
    return redemption


def list_reward_redemptions(db: Session) -> list[RewardRedemption]:
    return db.query(RewardRedemption).all()


def add_notification(db: Session, message: str, notification_type: str, user_id: int | None = None) -> Notification:
    notification = Notification(message=message, notification_type=notification_type, user_id=user_id)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def list_notifications(db: Session, user_id: int | None = None) -> list[Notification]:
    query = db.query(Notification)
    if user_id is not None:
        query = query.filter(Notification.user_id == user_id)
    return query.all()


def get_dashboard_summary(db: Session) -> dict:
    carbon_logs = db.query(CarbonLog).all()
    carbon_transactions = db.query(CarbonTransaction).all()
    csr_activities = db.query(CSRActivityRecord).all()
    policies = db.query(Policy).all()
    issues = db.query(ComplianceIssue).all()
    challenges = db.query(Challenge).all()
    rewards = db.query(RewardRedemption).all()

    total_emissions = round(sum(log.amount for log in carbon_logs) + sum(transaction.emission_value for transaction in carbon_transactions), 1)
    csr_count = len(csr_activities)
    active_policies = len([p for p in policies if p.status == "active"])
    policy_ratio = (active_policies / len(policies)) if policies else 0.0
    open_issues = len([issue for issue in issues if issue.status not in {"Resolved", "Closed"}])
    active_challenges = len([challenge for challenge in challenges if challenge.status == "Active"])
    redeemed_rewards = len(rewards)

    environmental_score = max(0.0, min(100.0, 100 - total_emissions / 6))
    social_score = min(100.0, csr_count * 10.0 + active_challenges * 3.0)
    governance_score = round(policy_ratio * 100, 1)
    overall_score = round(environmental_score * 0.4 + social_score * 0.3 + governance_score * 0.3, 1)

    department_counts: dict[str, int] = {}
    for activity in csr_activities:
        department_counts[activity.department] = department_counts.get(activity.department, 0) + 1

    leaderboard = [
        {"name": name, "score": min(100, 40 + count * 12)}
        for name, count in sorted(department_counts.items(), key=lambda kv: kv[1], reverse=True)
    ] or [{"name": "No CSR activity yet", "score": 0}]

    return {
        "summary": [
            {"label": "Overall ESG Score", "value": f"{overall_score}/100", "delta": "Live", "tone": "positive" if overall_score >= 70 else "neutral"},
            {"label": "Carbon Emissions", "value": f"{total_emissions} units logged", "delta": f"{len(carbon_logs) + len(carbon_transactions)} entries", "tone": "neutral"},
            {"label": "CSR Activities", "value": str(csr_count), "delta": "Live", "tone": "positive" if csr_count > 0 else "neutral"},
            {"label": "Governance Status", "value": f"{active_policies}/{len(policies)} active", "delta": "Live", "tone": "positive" if policy_ratio >= 0.5 else "neutral"},
        ],
        "kpis": [
            {"name": "Environmental Score", "value": round(environmental_score, 1), "target": 100},
            {"name": "Social Score", "value": round(social_score, 1), "target": 100},
            {"name": "Governance Score", "value": governance_score, "target": 100},
            {"name": "Open compliance issues", "value": open_issues, "target": 10},
            {"name": "Active challenges", "value": active_challenges, "target": 10},
            {"name": "Rewards redeemed", "value": redeemed_rewards, "target": 20},
        ],
        "initiatives": [
            "Record more activity data to refine environmental estimates",
            "Launch additional CSR and challenge participation programs",
            "Publish active policies and close open compliance issues",
        ],
        "leaderboard": leaderboard,
    }
