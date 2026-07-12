from sqlalchemy.orm import Session
from app.database import Base, engine
from app.models.esg_models import User, CarbonLog, CSRActivity, Policy
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


def list_carbon_logs(db: Session) -> list[CarbonLog]:
    return db.query(CarbonLog).all()


def add_csr_activity(db: Session, title: str, description: str, location: str, organizer: str, user_id: int | None = None) -> CSRActivity:
    activity = CSRActivity(title=title, description=description, location=location, organizer=organizer, user_id=user_id)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def list_csr_activities(db: Session) -> list[CSRActivity]:
    return db.query(CSRActivity).all()


def add_policy(db: Session, title: str, description: str, version: str, status: str = "draft") -> Policy:
    policy = Policy(title=title, description=description, version=version, status=status)
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def list_policies(db: Session) -> list[Policy]:
    return db.query(Policy).all()


def get_dashboard_summary(db: Session) -> dict:
    """Compute real dashboard metrics from the database instead of static demo data."""
    carbon_logs = db.query(CarbonLog).all()
    csr_activities = db.query(CSRActivity).all()
    policies = db.query(Policy).all()

    total_emissions = round(sum(log.amount for log in carbon_logs), 1)
    csr_count = len(csr_activities)
    active_policies = len([p for p in policies if p.status == "active"])
    policy_ratio = (active_policies / len(policies)) if policies else 0.0

    # ESG sub-scores derived from real records (see project's default 40/30/30 weighting).
    environmental_score = max(0.0, min(100.0, 100 - total_emissions / 5))
    social_score = min(100.0, csr_count * 12.0)
    governance_score = round(policy_ratio * 100, 1)
    overall_score = round(
        environmental_score * 0.4 + social_score * 0.3 + governance_score * 0.3, 1
    )

    department_counts: dict[str, int] = {}
    for activity in csr_activities:
        department_counts[activity.organizer] = department_counts.get(activity.organizer, 0) + 1

    leaderboard = [
        {"name": name, "score": min(100, 40 + count * 15)}
        for name, count in sorted(department_counts.items(), key=lambda kv: kv[1], reverse=True)
    ] or [{"name": "No CSR activity yet", "score": 0}]

    return {
        "summary": [
            {
                "label": "Overall ESG Score",
                "value": f"{overall_score}/100",
                "delta": "Live",
                "tone": "positive" if overall_score >= 70 else "neutral",
            },
            {
                "label": "Carbon Emissions",
                "value": f"{total_emissions} units logged",
                "delta": f"{len(carbon_logs)} entries",
                "tone": "neutral",
            },
            {
                "label": "CSR Activities",
                "value": str(csr_count),
                "delta": "Live",
                "tone": "positive" if csr_count > 0 else "neutral",
            },
            {
                "label": "Governance Status",
                "value": f"{active_policies}/{len(policies)} active",
                "delta": "Live",
                "tone": "positive" if policy_ratio >= 0.5 else "neutral",
            },
        ],
        "kpis": [
            {"name": "Environmental Score", "value": round(environmental_score, 1), "target": 100},
            {"name": "Social Score", "value": round(social_score, 1), "target": 100},
            {"name": "Governance Score", "value": governance_score, "target": 100},
        ],
        "initiatives": [
            "Log more carbon data to sharpen the environmental score",
            "Add CSR activities to boost social score and leaderboard participation",
            "Publish and activate policies to improve governance score",
        ],
        "leaderboard": leaderboard,
    }
