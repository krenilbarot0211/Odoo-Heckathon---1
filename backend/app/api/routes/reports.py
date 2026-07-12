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
        ],
    )
