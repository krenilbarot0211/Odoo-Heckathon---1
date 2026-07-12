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
