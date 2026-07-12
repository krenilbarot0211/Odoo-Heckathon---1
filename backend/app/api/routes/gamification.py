from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.esg import BadgeRequest, ChallengeParticipationRequest, ChallengeRequest, RewardRedemptionRequest, RewardRequest
from app.services.db_service import add_badge, add_challenge, add_challenge_participation, add_notification, add_reward, list_badges, list_challenges, list_reward_redemptions, list_rewards, redeem_reward

router = APIRouter()


@router.get("/challenges")
async def list_challenge_routes(db: Session = Depends(get_db)) -> list:
    challenges = list_challenges(db)
    return [{
        "id": item.id,
        "title": item.title,
        "category": item.category,
        "xp_reward": item.xp_reward,
        "difficulty": item.difficulty,
        "evidence_required": item.evidence_required,
        "deadline": item.deadline,
        "status": item.status,
    } for item in challenges]


@router.post("/challenge")
async def create_challenge(payload: ChallengeRequest, db: Session = Depends(get_db)) -> dict:
    challenge = add_challenge(
        db,
        payload.title,
        payload.category,
        payload.description,
        payload.xp_reward,
        payload.difficulty,
        payload.evidence_required,
        payload.deadline,
        payload.status,
    )
    return {"message": "Challenge created", "data": {"id": challenge.id, "title": challenge.title}}


@router.post("/challenge-participation")
async def create_challenge_participation(payload: ChallengeParticipationRequest, db: Session = Depends(get_db)) -> dict:
    if payload.approval_status == "Approved" and not payload.proof_attachment:
        raise HTTPException(status_code=400, detail="Proof is required for approved challenge participation")
    participation = add_challenge_participation(
        db,
        payload.challenge_id,
        payload.employee,
        payload.progress,
        payload.proof_attachment,
        payload.approval_status,
        payload.xp_awarded,
        payload.completion_date,
    )
    add_notification(db, f"Challenge participation submitted for {payload.employee}", "challenge_submission", participation.user_id)
    return {"message": "Challenge participation recorded", "data": {"id": participation.id}}


@router.get("/badges")
async def list_badges_route(db: Session = Depends(get_db)) -> list:
    badges = list_badges(db)
    return [{"id": item.id, "name": item.name, "unlock_metric": item.unlock_metric, "unlock_value": item.unlock_value, "status": item.status} for item in badges]


@router.post("/badge")
async def create_badge(payload: BadgeRequest, db: Session = Depends(get_db)) -> dict:
    badge = add_badge(db, payload.name, payload.description, payload.icon, payload.unlock_metric, payload.unlock_value, payload.status)
    return {"message": "Badge created", "data": {"id": badge.id, "name": badge.name}}


@router.get("/rewards")
async def list_rewards_route(db: Session = Depends(get_db)) -> list:
    rewards = list_rewards(db)
    return [{"id": item.id, "name": item.name, "points_required": item.points_required, "stock": item.stock, "status": item.status} for item in rewards]


@router.post("/reward")
async def create_reward(payload: RewardRequest, db: Session = Depends(get_db)) -> dict:
    reward = add_reward(db, payload.name, payload.description, payload.points_required, payload.stock, payload.status)
    return {"message": "Reward created", "data": {"id": reward.id, "name": reward.name}}


@router.post("/redeem")
async def redeem_reward_route(payload: RewardRedemptionRequest, db: Session = Depends(get_db)) -> dict:
    try:
        redemption = redeem_reward(db, payload.reward_id, None, payload.points_used)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"message": "Reward redeemed", "data": {"id": redemption.id, "status": redemption.status}}


@router.get("/redemptions")
async def list_redemptions(db: Session = Depends(get_db)) -> list:
    redemptions = list_reward_redemptions(db)
    return [{"id": item.id, "reward_id": item.reward_id, "points_used": item.points_used, "status": item.status} for item in redemptions]