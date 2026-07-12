from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

SECRET_KEY = "ecosphere-dev-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ROLE_PERMISSIONS = {
    "administrator": ["view_dashboard", "manage_users", "publish_policy", "submit_csr", "approve_reports"],
    "esg_manager": ["view_dashboard", "publish_policy", "submit_csr", "approve_reports"],
    "department_manager": ["view_dashboard", "submit_csr", "view_reports"],
    "employee": ["view_dashboard", "submit_csr"],
    "auditor": ["view_dashboard", "view_reports", "audit_logs"],
}


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_role_permissions(role: str) -> list[str]:
    return ROLE_PERMISSIONS.get(role.lower(), ROLE_PERMISSIONS["employee"])
