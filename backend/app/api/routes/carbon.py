from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import CarbonLogRequest, CarbonTransactionRequest
from app.services.db_service import add_carbon_log, add_carbon_transaction, list_carbon_logs, list_carbon_transactions

router = APIRouter()


@router.get("/analytics")
async def carbon_analytics(db: Session = Depends(get_db)) -> dict:
    logs = list_carbon_logs(db)
    transactions = list_carbon_transactions(db)
    return {
        "total_logs": len(logs),
        "logs": [{"id": log.id, "source": log.source, "amount": log.amount, "unit": log.unit, "date": log.date} for log in logs],
        "transactions": [{"id": txn.id, "source": txn.source, "emission_value": txn.emission_value, "transaction_date": txn.transaction_date} for txn in transactions],
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


@router.post("/transaction")
async def create_carbon_transaction(payload: CarbonTransactionRequest, db: Session = Depends(get_db)) -> dict:
    transaction = add_carbon_transaction(
        db,
        payload.source,
        payload.activity_quantity,
        payload.emission_factor,
        payload.transaction_date,
        payload.description,
    )
    return {"message": "Carbon transaction recorded", "data": {"id": transaction.id, "emission_value": transaction.emission_value}}
