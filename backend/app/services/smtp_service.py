import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
DEFAULT_RECIPIENT = os.getenv("EMAIL_TO", "kapnangcynthia@gmail.com")


class SMTPEmailService:
    def send_email(self, subject: str, body: str, to_email: str = DEFAULT_RECIPIENT) -> dict:
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            return {
                "status": "mocked",
                "to": to_email,
                "subject": subject,
                "body": body,
                "message": "SMTP non configuré. Mail simulé en mode dev.",
            }

        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = SMTP_USERNAME
            msg["To"] = to_email
            msg.set_content(body)

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)

            return {
                "status": "sent",
                "to": to_email,
                "subject": subject,
                "message": "Email envoyé avec succès.",
            }
        except Exception as exc:  # pragma: no cover
            return {
                "status": "error",
                "to": to_email,
                "subject": subject,
                "message": str(exc),
            }
