from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health", response_class=JSONResponse, tags=["health"])
def health_check():
    """Return a simple readiness payload."""
    return {"status": "ok", "service": "RegionGuard"}
