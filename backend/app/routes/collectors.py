from fastapi import APIRouter

from app.services.collector_service import collector_service

router = APIRouter(prefix="/collectors", tags=["collectors"])


@router.get("/status")
def collector_status():
    return {
        "status": "ok",
        "jobs_seen": len(collector_service.jobs),
        "seen_signatures": len(collector_service.seen_signatures),
    }


@router.post("/run")
def run_collectors():
    return collector_service.run_all()
