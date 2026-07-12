from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import AuthResponse, LoginRequest, RegisterRequest
from app.services.db_service import authenticate_user, create_user

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return AuthResponse(access_token="demo-token", user={"id": user.id, "name": user.name, "email": user.email, "role": user.role, "department": user.department})


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    user = create_user(db, payload.name, payload.email, payload.password, payload.role)
    return AuthResponse(access_token="demo-token", user={"id": user.id, "name": user.name, "email": user.email, "role": user.role, "department": user.department})
