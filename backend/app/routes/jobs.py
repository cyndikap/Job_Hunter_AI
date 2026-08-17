from fastapi import APIRouter

from app.services.brevo import brevo_service
from app.services.matching import match_engine
from app.services.scanning import scan_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/sample")
def get_sample_jobs():
    jobs = []
    for source in scan_service.sources:
        jobs.extend(source.fetch_jobs())
    return {"jobs": jobs}


@router.post("/scan")
async def trigger_scan():
    return scan_service.scan()


@router.post("/match")
async def match_job(job: dict):
    result = match_engine.calculate(job)
    return {
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "match": result,
    }


@router.post("/alert")
async def send_alert(payload: dict):
    match = match_engine.calculate(payload)
    alert_payload = {
        "title": payload.get("title", ""),
        "company": payload.get("company", ""),
        "score": round(match["score_overall"], 2),
        "common_skills": match.get("common_skills", []),
        "url": payload.get("url", "#"),
    }
    email_response = await brevo_service.send_alert(alert_payload)
    return {"status": "ok", "email": email_response}
