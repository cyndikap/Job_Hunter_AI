from app.crm.email_classifier import EmailClassifier
from app.crm.status_service import ApplicationStatusService


def test_status_transition_and_follow_up_rule():
    next_status = ApplicationStatusService.transition("APPLIED", "FOLLOW_UP_SENT")
    assert next_status == "FOLLOW_UP_SENT"
    assert ApplicationStatusService.should_send_follow_up("APPLIED", 7) is True


def test_email_classifier_detects_interview_request():
    label, confidence = EmailClassifier.classify(
        "Entretien RH",
        "Bonjour, nous souhaiterions vous proposer un entretien avec l'équipe RH demain matin.",
    )
    assert label == "INTERVIEW_REQUEST"
    assert confidence >= 0.9
