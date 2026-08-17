from datetime import datetime, timedelta, timezone
from fastapi import APIRouter

from app.services.scanning import scan_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary():
    jobs = scan_service.jobs
    window_start = datetime.now(timezone.utc) - timedelta(minutes=30)
    recent_jobs = [job for job in jobs if job.get("detected_at") and datetime.fromisoformat(job["detected_at"]).astimezone(timezone.utc) >= window_start]

    top_opportunities = sorted(jobs, key=lambda item: float(item.get("match_score", 0)), reverse=True)[:5]
    best = top_opportunities[0] if top_opportunities else {}

    return {
        "candidate": "Cynthia Sileu Kapnang",
        "role_target": "AI & Data Engineer",
        "jobs_monitored": len(jobs),
        "high_match": sum(1 for job in jobs if float(job.get("match_score", 0)) >= 80),
        "medium_match": sum(1 for job in jobs if 65 <= float(job.get("match_score", 0)) < 80),
        "low_match": sum(1 for job in jobs if float(job.get("match_score", 0)) < 65),
        "new_jobs_today": sum(1 for job in jobs if job.get("source") and job.get("detected_at")),
        "jobs_detected_in_30m": len(recent_jobs),
        "top_opportunities": top_opportunities,
        "best_opportunity": best,
        "last_scan": max((job.get("detected_at") for job in jobs), default=datetime.now(timezone.utc).isoformat()),
        "alerts": [
            {
                "id": job.get("id", idx),
                "type": "email",
                "company": job.get("company", "-"),
                "title": job.get("title", "-") ,
                "score": float(job.get("match_score", 0)),
                "status": "Envoyé" if float(job.get("match_score", 0)) >= 80 else "À surveiller",
                "date": job.get("detected_at", datetime.now(timezone.utc).isoformat()),
            }
            for idx, job in enumerate(jobs[:5])
        ],
    }
