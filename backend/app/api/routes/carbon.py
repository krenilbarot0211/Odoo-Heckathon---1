from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import CarbonLogRequest
from app.services.db_service import add_carbon_log, list_carbon_logs

router = APIRouter()


@router.get("/analytics")
async def carbon_analytics(db: Session = Depends(get_db)) -> dict:
    logs = list_carbon_logs(db)
    return {
        "total_logs": len(logs),
        "logs": [{"id": log.id, "source": log.source, "amount": log.amount, "unit": log.unit, "date": log.date} for log in logs],
        "trend": [
            {"month": "Apr", "value": 13.6},
            {"month": "May", "value": 12.9},
            {"month": "Jun", "value": 12.4},
        ],
    }


@router.post("/log")
async def log_carbon(payload: CarbonLogRequest, db: Session = Depends(get_db)) -> dict:
    log = add_carbon_log(db, payload.source, payload.amount, payload.unit, payload.date)
    return {"message": "Carbon log recorded", "data": {"id": log.id, "source": log.source, "amount": log.amount, "unit": log.unit, "date": log.date}}
