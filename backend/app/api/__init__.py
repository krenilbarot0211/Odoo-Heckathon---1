from fastapi import APIRouter
from app.api.routes import auth, carbon, csr, governance, reports

router = APIRouter(prefix="/api")
router.include_router(auth.router, prefix="/auth")
router.include_router(carbon.router, prefix="/carbon")
router.include_router(csr.router, prefix="/csr")
router.include_router(governance.router, prefix="/governance")
router.include_router(reports.router, prefix="/reports")
