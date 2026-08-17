from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.security.jwt_auth import get_current_user
from app.services.analytics_service import analytics_service
from app.services.notifications_service import notification_center

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
def get_ai_insights(current_user: dict = Depends(get_current_user)):
    metrics = analytics_service.calculate_dashboard_metrics()
    notifications = notification_center.get_notifications()
    return {
        "user_id": current_user.get("user_id"),
        "career_score": metrics["career_score"],
        "response_rate": metrics["response_rate"],
        "interview_rate": metrics["interview_rate"],
        "hire_rate": metrics["hire_rate"],
        "average_response_time_days": metrics["average_response_time_days"],
        "most_reactive_company": metrics["most_reactive_company"],
        "most_efficient_source": metrics["most_efficient_source"],
        "most_demanded_technology": metrics["most_demanded_technology"],
        "top_opportunities": metrics["top_opportunities"],
        "missing_skills": metrics["missing_skills"],
        "notifications": notifications,
    }


@router.get("/summary")
def get_analytics_summary(current_user: dict = Depends(get_current_user)):
    if not current_user.get("user_id"):
        raise HTTPException(status_code=400, detail="user_id is required")
    return analytics_service.calculate_dashboard_metrics()
