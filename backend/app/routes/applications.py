from fastapi import APIRouter

router = APIRouter(prefix="/applications", tags=["applications"])

APPLICATIONS = [
    {
        "id": 1,
        "date": "2026-08-15",
        "company": "Ippon Technologies",
        "status": "Email envoyé",
        "score": 92,
        "link": "https://example.com/job/1",
    },
    {
        "id": 2,
        "company": "Capgemini",
        "status": "En attente",
        "score": 88,
        "date": "2026-08-14",
        "link": "https://example.com/job/2",
    },
]


@router.get("/list")
def list_applications():
    return {"applications": APPLICATIONS}


@router.post("/create")
def create_application(application: dict):
    application["id"] = len(APPLICATIONS) + 1
    application.setdefault("status", "new")
    application.setdefault("date", "2026-08-15")
    APPLICATIONS.append(application)
    return {"status": "created", "application": application}
