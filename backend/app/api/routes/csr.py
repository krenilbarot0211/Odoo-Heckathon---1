from fastapi import APIRouter
from app.schemas.esg import CSRActivityRequest
from app.services.esg_store import store

router = APIRouter()


@router.get("/activities")
async def list_activities() -> list:
    return store.list_csr_activities()


@router.post("/activity")
async def create_activity(payload: CSRActivityRequest) -> dict:
    return {"message": "CSR activity created", "data": store.add_csr_activity(payload.model_dump())}
