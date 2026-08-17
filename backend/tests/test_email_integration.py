import app.services.smtp_service as smtp_service
from app.services.imap_service import IMAPEmailService


def test_imap_email_classification_detects_interview_response():
    service = IMAPEmailService()
    result = service.classify_message(
        {
            "subject": "Entretien technique confirmé",
            "from": "recruteur@company.com",
            "body": "Bonjour, merci pour votre candidature. Nous vous proposons un entretien technique le mardi prochain.",
        }
    )

    assert result["status"] == "interview"
    assert result["provider"] == "recruiter"
    assert "interview" in result["keywords"]


def test_imap_email_classification_detects_rejection():
    service = IMAPEmailService()
    result = service.classify_message(
        {
            "subject": "Refus de candidature",
            "from": "jobs@company.com",
            "body": "Merci pour votre intérêt, nous avons décidé de ne pas poursuivre votre candidature.",
        }
    )

    assert result["status"] == "rejected"
    assert "refus" in result["summary"].lower()


def test_smtp_email_is_mocked_when_credentials_missing(monkeypatch):
    monkeypatch.setattr(smtp_service, "SMTP_USERNAME", "")
    monkeypatch.setattr(smtp_service, "SMTP_PASSWORD", "")

    result = smtp_service.SMTPEmailService().send_email(
        "Test Job Hunter",
        "Corps exemple",
        "candidate@example.com",
    )

    assert result["status"] == "mocked"
    assert result["to"] == "candidate@example.com"
    assert "simulé" in result["message"].lower()


def test_smtp_email_is_sent_when_credentials_are_configured(monkeypatch):
    class DummySMTP:
        def __init__(self, host, port):
            self.host = host
            self.port = port

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            return None

        def login(self, username, password):
            assert username == "user@example.com"
            assert password == "secret"

        def send_message(self, message):
            assert message["To"] == "candidate@example.com"
            assert message["Subject"] == "Test Job Hunter"

    monkeypatch.setattr(smtp_service, "SMTP_HOST", "smtp.example.com")
    monkeypatch.setattr(smtp_service, "SMTP_PORT", 587)
    monkeypatch.setattr(smtp_service, "SMTP_USERNAME", "user@example.com")
    monkeypatch.setattr(smtp_service, "SMTP_PASSWORD", "secret")
    monkeypatch.setattr(smtp_service.smtplib, "SMTP", DummySMTP)

    result = smtp_service.SMTPEmailService().send_email(
        "Test Job Hunter",
        "Corps exemple",
        "candidate@example.com",
    )

    assert result["status"] == "sent"
    assert result["to"] == "candidate@example.com"
    assert "succès" in result["message"].lower()
