from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import CSRActivityRequest
from app.services.db_service import add_csr_activity, list_csr_activities

router = APIRouter()


@router.get("/activities")
async def list_activities(db: Session = Depends(get_db)) -> list:
    activities = list_csr_activities(db)
    return [{"id": item.id, "title": item.title, "description": item.description, "location": item.location, "organizer": item.organizer} for item in activities]


@router.post("/activity")
async def create_activity(payload: CSRActivityRequest, db: Session = Depends(get_db)) -> dict:
    activity = add_csr_activity(db, payload.title, payload.description, payload.location, payload.organizer)
    return {"message": "CSR activity created", "data": {"id": activity.id, "title": activity.title, "location": activity.location, "organizer": activity.organizer}}
