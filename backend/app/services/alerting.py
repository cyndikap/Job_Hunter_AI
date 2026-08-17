from datetime import datetime
from typing import Dict, List

from app.services.smtp_service import SMTPEmailService

DEFAULT_EMAIL = "kapnangcynthia@gmail.com"
EMAIL_THRESHOLD = 85


class AlertService:
    def __init__(self):
        self.sent_urls: set[str] = set()
        self.smtp = SMTPEmailService()

    def should_send(self, job_url: str, score: int) -> bool:
        return score >= EMAIL_THRESHOLD and job_url not in self.sent_urls

    def mark_sent(self, job_url: str) -> None:
        self.sent_urls.add(job_url)

    def build_email(self, job: Dict[str, object]) -> str:
        title = job.get("title", "Offre détectée")
        company = job.get("company", "-")
        location = job.get("location", "-")
        score = job.get("match_score", 0)
        skills = ", ".join(job.get("skills", []))
        url = job.get("url", "")

        return (
            "Offre détectée\n"
            "\n"
            f"Poste: {title}\n"
            f"Entreprise: {company}\n"
            f"Localisation: {location}\n"
            f"Score de matching: {score} %\n"
            f"Compétences détectées: {skills}\n"
            f"Lien: {url}\n"
            "\n"
            "Merci de considérer cette opportunité."
        )

    def build_daily_summary(self, jobs: List[Dict[str, object]]) -> str:
        if not jobs:
            return "Récapitulatif quotidien Job Hunter AI\nAucune offre pertinente n'a été détectée aujourd'hui."

        lines = ["Récapitulatif quotidien Job Hunter AI", ""]
        for job in jobs:
            lines.append(
                f"- {job.get('title')} | {job.get('company')} | {job.get('location')} | "
                f"Score {job.get('match_score')}% | {', '.join(job.get('skills', []))}"
            )
        return "\n".join(lines)

    def build_linkedin_message(self, job: Dict[str, object]) -> str:
        title = job.get("title", "Offre")
        company = job.get("company", "entreprise")
        score = job.get("match_score", 0)
        url = job.get("url", "")
        return (
            "Bonjour,\n\n"
            f"Je suis très intéressé(e) par l’offre {title} chez {company}.\n"
            f"Mon profil montre une compatibilité de {score}% avec ce poste, notamment sur Azure, Data, IA et RAG.\n"
            f"Je serais ravi(e) de discuter davantage. Vous trouverez le poste ici : {url}\n\n"
            "Cordialement,\nCynthia Sileu Kapnang"
        )

    def build_plain_text_flow(self, job: Dict[str, object]) -> str:
        return (
            "Offre détectée\n"
            "↓\n"
            f"Matching {job.get('match_score', 0)} %\n"
            "↓\n"
            "Email généré\n"
            "↓\n"
            "Message LinkedIn généré\n"
        )

    def send_email(self, job: Dict[str, object]) -> Dict[str, object]:
        job_url = str(job.get("url", ""))
        score = int(job.get("match_score", 0))
        if not self.should_send(job_url, score):
            return {"status": "skipped", "reason": "already sent or below threshold"}

        self.mark_sent(job_url)
        smtp_result = self.smtp.send_email(
            subject=f"Job Hunter AI - {job.get('title', 'Nouvelle opportunité')}",
            body=self.build_email(job),
            to_email=DEFAULT_EMAIL,
        )

        return {
            "status": smtp_result.get("status", "sent"),
            "channel": "email",
            "to": DEFAULT_EMAIL,
            "subject": f"Job Hunter AI - {job.get('title', 'Nouvelle opportunité')}",
            "body": self.build_email(job),
            "generated_at": datetime.utcnow().isoformat(),
            "smtp_result": smtp_result,
        }
