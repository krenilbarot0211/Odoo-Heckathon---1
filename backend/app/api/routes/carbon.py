from fastapi import APIRouter
from app.schemas.esg import CarbonLogRequest
from app.services.esg_store import store

router = APIRouter()


@router.get("/analytics")
async def carbon_analytics() -> dict:
    return {
        "total_logs": len(store.get_carbon_logs()),
        "logs": store.get_carbon_logs(),
        "trend": [
            {"month": "Apr", "value": 13.6},
            {"month": "May", "value": 12.9},
            {"month": "Jun", "value": 12.4},
        ],
    }


@router.post("/log")
async def log_carbon(payload: CarbonLogRequest) -> dict:
    return {"message": "Carbon log recorded", "data": store.add_carbon_log(payload.model_dump())}
