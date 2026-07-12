from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api import router as api_router
from app.database import get_db
from app.services.db_service import get_dashboard_summary

app = FastAPI(title="EcoSphere AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "ecosphere-ai"}


@app.get("/api/dashboard")
async def dashboard_data(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)
