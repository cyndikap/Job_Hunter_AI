from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.crm.service import CRMService

router = APIRouter(prefix="/crm", tags=["crm"])
crm_service = CRMService()

APPLICATIONS_DB: list[dict[str, Any]] = [
    {
        "id": "app-1",
        "user_id": "user-1",
        "job_id": "job-1",
        "status": "APPLIED",
        "source": "apec",
        "events": [
            {"created_at": "2026-08-10T09:20:00Z", "new_status": "DETECTED"},
            {"created_at": "2026-08-10T10:15:00Z", "new_status": "APPLIED"},
        ],
    },
    {
        "id": "app-2",
        "user_id": "user-1",
        "job_id": "job-2",
        "status": "HR_INTERVIEW",
        "source": "wttj",
        "events": [
            {"created_at": "2026-08-12T08:00:00Z", "new_status": "DETECTED"},
            {"created_at": "2026-08-15T09:00:00Z", "new_status": "HR_INTERVIEW"},
        ],
    },
]

RECRUITERS_DB: list[dict[str, Any]] = [
    {"id": "rec-1", "first_name": "Alice", "last_name": "Martin", "company": "Apex AI", "email": "alice@apex.ai"},
    {"id": "rec-2", "first_name": "Bob", "last_name": "Lemoine", "company": "North Data", "email": "bob@northdata.io"},
]

EMAILS_DB: list[dict[str, Any]] = [
    {"id": "mail-1", "application_id": "app-1", "direction": "incoming", "subject": "Entretien RH", "content": "Bonjour, nous souhaiterions vous proposer un entretien RH."},
]


@router.get("/applications")
def get_applications():
    return {"applications": APPLICATIONS_DB}


@router.get("/applications/{application_id}")
def get_application(application_id: str):
    for item in APPLICATIONS_DB:
        if item["id"] == application_id:
            return item
    raise HTTPException(status_code=404, detail="Application not found")


@router.post("/applications")
def create_application(payload: dict[str, Any]):
    new_app = {
        "id": f"app-{len(APPLICATIONS_DB) + 1}",
        "user_id": payload.get("user_id", "user-1"),
        "job_id": payload.get("job_id"),
        "status": payload.get("status", "DETECTED"),
        "source": payload.get("source", "manual"),
        "events": [{"created_at": __import__("datetime").datetime.utcnow().isoformat(), "new_status": payload.get("status", "DETECTED")}],
    }
    APPLICATIONS_DB.append(new_app)
    return {"status": "created", "application": new_app}


@router.patch("/applications/{application_id}/status")
def update_application_status(application_id: str, payload: dict[str, Any]):
    for item in APPLICATIONS_DB:
        if item["id"] == application_id:
            updated = crm_service.update_application_status(item, payload["status"])
            return {"status": "updated", "application": updated}
    raise HTTPException(status_code=404, detail="Application not found")


@router.get("/applications/{application_id}/timeline")
def get_application_timeline(application_id: str):
    app = next((item for item in APPLICATIONS_DB if item["id"] == application_id), None)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"application_id": application_id, "timeline": crm_service.build_timeline(app.get("events", []))}


@router.get("/recruiters")
def list_recruiters():
    return {"recruiters": RECRUITERS_DB}


@router.post("/recruiters")
def create_recruiter(payload: dict[str, Any]):
    recruiter = {"id": f"rec-{len(RECRUITERS_DB) + 1}", **payload}
    RECRUITERS_DB.append(recruiter)
    return {"status": "created", "recruiter": recruiter}


@router.get("/emails")
def list_emails():
    return {"emails": EMAILS_DB}


@router.post("/emails/send")
def send_email(payload: dict[str, Any]):
    email = {
        "id": f"mail-{len(EMAILS_DB) + 1}",
        "application_id": payload.get("application_id"),
        "recruiter_id": payload.get("recruiter_id"),
        "direction": "outgoing",
        "subject": payload.get("subject", "Relance candidature"),
        "content": payload.get("content", "Bonjour, je vous relance concernant ma candidature."),
    }
    EMAILS_DB.append(email)
    return {"status": "sent", "email": email}
