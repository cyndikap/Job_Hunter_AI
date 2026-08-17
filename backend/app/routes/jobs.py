from fastapi import APIRouter

from app.services.alerting import AlertService
from app.services.job_matcher import score_job
from app.services.openai_agent import AIJobAssistant

router = APIRouter(prefix="/jobs", tags=["jobs"])
alert_service = AlertService()
assistant = AIJobAssistant()

PROFILE_JOB_EXAMPLES = [
    {
        "id": 1,
        "title": "AI Engineer",
        "company": "Ippon Technologies",
        "location": "Paris / Remote",
        "match_score": 92,
        "classification": "Très forte adéquation",
        "skills": ["Azure Databricks", "LLM", "RAG", "MLflow", "Python"],
        "url": "https://example.com/job/1",
    },
    {
        "id": 2,
        "title": "Data & AI Engineer",
        "company": "Capgemini",
        "location": "Paris",
        "match_score": 88,
        "classification": "Forte adéquation",
        "skills": ["Azure", "Python", "SQL", "Data Governance", "FastAPI"],
        "url": "https://example.com/job/2",
    },
]


@router.get("/sample")
def get_sample_jobs():
    return {"jobs": PROFILE_JOB_EXAMPLES}


@router.post("/scan")
def trigger_scan():
    return {
        "status": "accepted",
        "message": "Le scan des offres a été déclenché.",
    }


@router.post("/match")
def match_job(job: dict):
    skills = job.get("skills", [])
    result = score_job(
        title=job.get("title", ""),
        company=job.get("company", ""),
        skills=skills,
        location=job.get("location", ""),
    )

    outcome = {
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "match_score": result["score"],
        "classification": result["classification"],
        "skills": skills,
        "summary": assistant.summarize_job(
            job.get("title", ""),
            job.get("company", ""),
            job.get("description", "Poste orienté IA, données et Azure."),
        ),
        "email": assistant.build_email(job),
        "linkedin_message": assistant.build_linkedin_message(job),
        "alert_triggered": result["score"] >= 85,
    }

    if outcome["alert_triggered"]:
        alert = alert_service.send_email({
            "title": outcome["title"],
            "company": outcome["company"],
            "location": outcome["location"],
            "match_score": outcome["match_score"],
            "skills": outcome["skills"],
            "url": job.get("url", ""),
        })
        outcome["alert_result"] = alert

    return outcome
