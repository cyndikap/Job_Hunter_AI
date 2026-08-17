from __future__ import annotations


def generate_linkedin_message(profile: dict, job: dict, recruiter: dict | None = None) -> str:
    full_name = profile.get("full_name", "Candidat")
    company = job.get("company", "Entreprise")
    title = job.get("title", "poste")
    recruiter_name = recruiter.get("first_name", "") if recruiter else ""
    return (
        f"Bonjour {recruiter_name or 'recruteur'},\n\n"
        f"Je suis {full_name} et je suis très intéressé(e) par le poste de {title} chez {company}.\n"
        "Je souhaiterais échanger avec vous sur mon profil et sur la candidature.\n\n"
        f"Vous trouverez le lien vers l'offre ici : {job.get('url', '')}\n\n"
        "Cordialement,\n"
        f"{full_name}"
    )


def generate_application_email(profile: dict, job: dict) -> str:
    full_name = profile.get("full_name", "Candidat")
    return (
        f"Objet : Candidature pour le poste {job.get('title', 'poste')}\n\n"
        f"Bonjour,\n\n"
        f"Je vous adresse ma candidature pour le poste {job.get('title', 'poste')} chez {job.get('company', 'l\'entreprise')}.\n"
        "Je suis très motivé(e) par cette opportunité et je suis convaincu(e) que mon profil correspond aux attentes.\n\n"
        "Cordialement,\n"
        f"{full_name}"
    )


def generate_follow_up_email(profile: dict, recruiter: dict | None = None) -> str:
    full_name = profile.get("full_name", "Candidat")
    recruiter_name = recruiter.get("first_name", "") if recruiter else ""
    return (
        f"Bonjour {recruiter_name or 'recruteur'},\n\n"
        "Je me permets de vous relancer afin de savoir le statut de ma candidature.\n"
        "Je reste très motivé(e) par cette opportunité et serais ravi(e) de poursuivre la discussion.\n\n"
        "Cordialement,\n"
        f"{full_name}"
    )
