from app.crm.email_classifier import EmailClassifier
from app.crm.service import CRMService


def test_email_incoming_to_classification_to_crm_update():
    email_text = "Bonjour, nous souhaiterions vous proposer un entretien technique vendredi à 10h."
    classification, confidence = EmailClassifier.classify("Entretien technique", email_text)
    crm = CRMService()
    update = crm.classify_incoming_email("Entretien technique", email_text)

    assert classification == "INTERVIEW_REQUEST"
    assert confidence >= 0.9
    assert update["classification"] == "INTERVIEW_REQUEST"
    assert update["confidence_score"] >= 0.9


def test_follow_up_triggered_after_seven_days():
    crm = CRMService()
    assert crm.should_send_follow_up("APPLIED", 7) is True
    assert crm.should_send_follow_up("APPLIED", 6) is False
