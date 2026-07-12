from fastapi import APIRouter, HTTPException
from app.schemas.esg import AuthResponse, LoginRequest, RegisterRequest
from app.services.esg_store import store

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest) -> AuthResponse:
    user = store.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return AuthResponse(access_token="demo-token", user=user)


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest) -> AuthResponse:
    user = store.register(payload.name, payload.email, payload.password, payload.role)
    return AuthResponse(access_token="demo-token", user=user)
