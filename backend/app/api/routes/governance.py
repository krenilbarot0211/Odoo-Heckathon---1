from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import ComplianceIssueRequest, GovernanceAuditRequest, GovernancePolicyRequest
from app.services.db_service import add_compliance_issue, add_governance_audit, add_notification, add_policy, add_policy_acknowledgement, list_compliance_issues, list_policies

router = APIRouter()


@router.get("/policies")
async def list_policies_route(db: Session = Depends(get_db)) -> list:
    policies = list_policies(db)
    return [{"id": item.id, "title": item.title, "description": item.description, "version": item.version, "status": item.status} for item in policies]


@router.post("/policy")
async def create_policy(payload: GovernancePolicyRequest, db: Session = Depends(get_db)) -> dict:
    policy = add_policy(db, payload.title, payload.description, payload.version, payload.status)
    return {"message": "Policy published", "data": {"id": policy.id, "title": policy.title, "version": policy.version, "status": policy.status}}


@router.post("/acknowledge")
async def acknowledge_policy(policy_id: int, user_id: int, db: Session = Depends(get_db)) -> dict:
    acknowledgement = add_policy_acknowledgement(db, policy_id, user_id, "Acknowledged", "2026-07-12", "Sent")
    return {"message": "Policy acknowledged", "data": {"id": acknowledgement.id, "status": acknowledgement.acknowledgement_status}}


@router.post("/audit")
async def create_audit(payload: GovernanceAuditRequest, db: Session = Depends(get_db)) -> dict:
    audit = add_governance_audit(
        db,
        payload.title,
        payload.department,
        payload.auditor,
        payload.start_date,
        payload.end_date,
        payload.status,
        payload.findings,
        payload.governance_score,
    )
    return {"message": "Audit created", "data": {"id": audit.id, "status": audit.status}}


@router.post("/compliance")
async def create_compliance_issue(payload: ComplianceIssueRequest, db: Session = Depends(get_db)) -> dict:
    if not payload.assigned_owner or not payload.due_date:
        raise HTTPException(status_code=400, detail="Assigned owner and due date are required")
    overdue_flag = payload.status not in {"Resolved", "Closed"} and payload.due_date < "2026-07-12"
    issue = add_compliance_issue(
        db,
        payload.related_audit_id,
        payload.severity,
        payload.description,
        payload.assigned_owner,
        payload.due_date,
        payload.status,
        payload.resolution_notes,
        overdue_flag,
    )
    add_notification(db, f"New compliance issue: {payload.description}", "compliance_issue", issue.user_id)
    return {"message": "Compliance issue recorded", "data": {"id": issue.id, "overdue": issue.overdue_flag}}
