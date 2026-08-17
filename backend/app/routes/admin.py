from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.security.jwt_auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview")
def get_admin_overview(current_user: dict = Depends(get_current_user)):
    allowed_ids = {item.strip() for item in settings.admin_user_ids.split(",") if item.strip()}
    user_id = str(current_user.get("user_id") or "")
    if user_id not in allowed_ids:
        raise HTTPException(status_code=403, detail="admin access required")

    return {
        "tenant": "job-hunter-ai",
        "users": 128,
        "active_sessions": 42,
        "indexed_documents": 864,
        "vector_count": 12600,
        "llm_errors_last_24h": 3,
        "avg_llm_latency_ms": 1840,
        "system_status": "healthy",
    }
