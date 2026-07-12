from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import GovernancePolicyRequest
from app.services.db_service import add_policy, list_policies

router = APIRouter()


@router.get("/policies")
async def list_policies_route(db: Session = Depends(get_db)) -> list:
    policies = list_policies(db)
    return [{"id": item.id, "title": item.title, "description": item.description, "version": item.version, "status": item.status} for item in policies]


@router.post("/policy")
async def create_policy(payload: GovernancePolicyRequest, db: Session = Depends(get_db)) -> dict:
    policy = add_policy(db, payload.title, payload.description, payload.version, payload.status)
    return {"message": "Policy published", "data": {"id": policy.id, "title": policy.title, "version": policy.version, "status": policy.status}}
