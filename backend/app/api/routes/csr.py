from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import CSRActivityDetailRequest, CSRActivityRequest, CSRParticipationRequest
from app.services.db_service import add_csr_activity, add_csr_activity_record, add_csr_participation, add_notification, list_csr_activities, list_csr_activity_records, list_csr_participations

router = APIRouter()


@router.get("/activities")
async def list_activities(db: Session = Depends(get_db)) -> list:
    activities = list_csr_activities(db)
    return [{"id": item.id, "title": item.title, "description": item.description, "location": item.location, "organizer": item.organizer} for item in activities]


@router.post("/activity")
async def create_activity(payload: CSRActivityRequest, db: Session = Depends(get_db)) -> dict:
    activity = add_csr_activity(db, payload.title, payload.description, payload.location, payload.organizer)
    return {"message": "CSR activity created", "data": {"id": activity.id, "title": activity.title, "location": activity.location, "organizer": activity.organizer}}


@router.get("/records")
async def list_activity_records(db: Session = Depends(get_db)) -> list:
    records = list_csr_activity_records(db)
    return [{
        "id": item.id,
        "title": item.title,
        "category": item.category,
        "department": item.department,
        "location": item.location,
        "organizer": item.organizer,
        "points": item.points,
        "evidence_required": item.evidence_required,
        "status": item.status,
    } for item in records]


@router.post("/record")
async def create_activity_record(payload: CSRActivityDetailRequest, db: Session = Depends(get_db)) -> dict:
    record = add_csr_activity_record(
        db,
        payload.title,
        payload.description,
        payload.category,
        payload.department,
        payload.location,
        payload.organizer,
        payload.start_date,
        payload.end_date,
        payload.max_participants,
        payload.points,
        payload.evidence_required,
        payload.status,
    )
    return {"message": "CSR activity record created", "data": {"id": record.id, "title": record.title, "points": record.points}}


@router.get("/participations")
async def list_participations(db: Session = Depends(get_db)) -> list:
    participations = list_csr_participations(db)
    return [{
        "id": item.id,
        "activity_id": item.activity_id,
        "employee": item.employee,
        "approval_status": item.approval_status,
        "points_earned": item.points_earned,
        "completion_date": item.completion_date,
    } for item in participations]


@router.post("/participation")
async def create_participation(payload: CSRParticipationRequest, db: Session = Depends(get_db)) -> dict:
    if payload.approval_status == "Approved" and not payload.proof_attachment:
        raise HTTPException(status_code=400, detail="Proof is required for approved participation")
    participation = add_csr_participation(
        db,
        payload.activity_id,
        payload.employee,
        payload.proof_attachment,
        payload.approval_status,
        payload.points_earned,
        payload.completion_date,
        payload.approval_remarks,
    )
    add_notification(db, f"CSR participation submitted for {payload.employee}", "csr_submission", participation.user_id)
    return {"message": "CSR participation recorded", "data": {"id": participation.id, "approval_status": participation.approval_status}}
