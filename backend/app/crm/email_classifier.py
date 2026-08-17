from __future__ import annotations

from app.crm.models import EmailClassification


class EmailClassifier:
    @staticmethod
    def classify(subject: str, content: str) -> tuple[str, float]:
        text = ((subject or "") + " " + (content or "")).lower()

        if any(token in text for token in ["interview", "rdv", "entretien", "call with us"]):
            return EmailClassification.INTERVIEW_REQUEST.value, 0.96
        if any(token in text for token in ["we are pleased", "we would like to move forward", "congratulations", "interested"]):
            return EmailClassification.POSITIVE_RESPONSE.value, 0.94
        if any(token in text for token in ["thank you", "we have decided to move forward with other candidates", "not selected", "rejected"]):
            return EmailClassification.REJECTION.value, 0.9
        if any(token in text for token in ["more information", "additional details", "can you share", "missing information"]):
            return EmailClassification.MORE_INFORMATION_REQUIRED.value, 0.88
        if any(token in text for token in ["follow up", "checking in", "follow-up", "just circling back"]):
            return EmailClassification.FOLLOW_UP.value, 0.82
        if any(token in text for token in ["newsletter", "promotion", "offer from", "win a prize"]):
            return EmailClassification.SPAM.value, 0.99
        return EmailClassification.AUTOMATIC_RESPONSE.value, 0.7
