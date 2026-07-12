from fastapi import APIRouter
from app.schemas.esg import ReportResponse

router = APIRouter()


@router.get("/generate", response_model=ReportResponse)
async def generate_report() -> ReportResponse:
    return ReportResponse(
        report_id="RPT-001",
        title="Quarterly ESG Summary",
        summary="The organization improved its ESG score by 6% and reduced emissions by 8% this quarter.",
        recommendations=[
            "Increase volunteer participation in underrepresented departments",
            "Expand rooftop solar projects for the next reporting cycle",
            "Accelerate policy renewal reminders for high-risk teams",
        ],
    )


@router.get("/analytics")
async def analytics_report() -> dict:
    return {
        "emissions_trend": [
            {"month": "Apr", "value": 13.6},
            {"month": "May", "value": 12.9},
            {"month": "Jun", "value": 12.4},
        ],
        "csr_trend": [
            {"month": "Apr", "value": 54},
            {"month": "May", "value": 63},
            {"month": "Jun", "value": 78},
        ],
        "governance_health": 94,
        "challenge_completion_rate": 72,
        "compliance_by_severity": [
            {"severity": "High", "count": 3},
            {"severity": "Medium", "count": 5},
            {"severity": "Low", "count": 2},
        ],
    }
