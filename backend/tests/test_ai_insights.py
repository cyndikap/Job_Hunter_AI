from app.services.analytics_service import AnalyticsService


def test_analytics_service_exposes_priority_metrics():
    service = AnalyticsService()
    metrics = service.calculate_dashboard_metrics()

    assert metrics["response_rate"] >= 0
    assert metrics["interview_rate"] >= 0
    assert "top_opportunities" in metrics
    assert "career_score" in metrics


def test_notifications_service_generates_alerts():
    from app.services.notifications_service import NotificationCenter

    center = NotificationCenter()
    alerts = center.get_notifications()

    assert len(alerts) >= 1
    assert any(item["type"] in {"new_offer", "interview", "follow_up", "no_response"} for item in alerts)
