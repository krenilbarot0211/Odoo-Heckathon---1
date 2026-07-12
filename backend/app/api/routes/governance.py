from fastapi import APIRouter
from app.schemas.esg import GovernancePolicyRequest
from app.services.esg_store import store

router = APIRouter()


@router.get("/policies")
async def list_policies() -> list:
    return store.list_policies()


@router.post("/policy")
async def create_policy(payload: GovernancePolicyRequest) -> dict:
    return {"message": "Policy published", "data": store.add_policy(payload.model_dump())}
