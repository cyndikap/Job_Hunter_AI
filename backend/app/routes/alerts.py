from fastapi import APIRouter

from app.services.alerting import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])
alert_service = AlertService()


@router.post("/check")
def check_alert(job: dict):
    score = int(job.get("match_score", 0))
    url = str(job.get("url", ""))
    if alert_service.should_send(url, score):
        result = alert_service.send_email(job)
        return {"status": "email_triggered", "result": result}
    return {"status": "not_sent", "reason": "below threshold or duplicate"}


@router.post("/daily-summary")
def daily_summary(jobs: list[dict]):
    return {"status": "ok", "summary": alert_service.build_daily_summary(jobs)}


@router.post("/linkedin")
def linkedin_generated(job: dict):
    return {"status": "generated", "message": alert_service.build_linkedin_message(job)}


@router.post("/flow")
def plain_text_flow(job: dict):
    return {"status": "ok", "flow": alert_service.build_plain_text_flow(job)}
