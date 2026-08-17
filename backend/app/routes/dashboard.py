from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary():
    return {
        "candidate": "Cynthia Sileu Kapnang",
        "role_target": "AI & Data Engineer",
        "jobs_monitored": 128,
        "high_match": 12,
        "medium_match": 30,
        "low_match": 86,
        "last_scan": "2026-08-15T08:00:00Z",
        "alerts": [
            {
                "id": 1,
                "type": "email",
                "company": "Ippon Technologies",
                "title": "AI Engineer",
                "score": 92,
                "status": "Envoyé",
                "date": "2026-08-15",
            },
            {
                "id": 2,
                "type": "email",
                "company": "Capgemini",
                "title": "Data & AI Engineer",
                "score": 88,
                "status": "Envoyé",
                "date": "2026-08-14",
            },
        ],
    }
