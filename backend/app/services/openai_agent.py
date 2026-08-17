from typing import Dict, List


class AIJobAssistant:
    def summarize_job(self, title: str, company: str, description: str) -> str:
        return (
            f"Poste: {title}\n"
            f"Entreprise: {company}\n"
            f"Résumé: Ce poste met l’accent sur la conception et la mise en production de pipelines de données, "
            "l’IA générative, la gouvernance des données et l’architecture cloud Azure."
            f"\nDétails: {description[:300]}..."
        )

    def extract_skills(self, text: str) -> List[str]:
        keywords = [
            "Azure Databricks",
            "Azure",
            "Python",
            "SQL",
            "RAG",
            "LLM",
            "Azure OpenAI",
            "Agentic AI",
            "MLflow",
            "MLOps",
            "FastAPI",
            "Data Governance",
            "MDM",
            "PIM",
            "Snowflake",
        ]
        found = [k for k in keywords if k.lower() in text.lower()]
        return found

    def build_cover_letter(self, job: Dict[str, object]) -> str:
        return (
            "Madame, Monsieur,\n\n"
            f"Je souhaite candidater au poste de {job.get('title', 'Data / AI Engineer')} chez {job.get('company', 'votre entreprise')}.\n"
            "Mon parcours est aligné avec les enjeux de Data Engineering, IA générative, gouvernance de données et architectures Azure.\n"
            "J’ai une forte appétence pour les sujets d’automatisation, de qualité des données, de RAG et d’agentic AI.\n"
            "Je serais ravi de contribuer à vos projets et de mettre mon expertise au service de vos objectifs.\n\n"
            "Cordialement,\nCynthia Sileu Kapnang"
        )

    def build_email(self, job: Dict[str, object]) -> str:
        title = job.get("title", "Nouvelle opportunité")
        company = job.get("company", "votre entreprise")
        url = job.get("url", "")
        return (
            f"Objet: Candidature pour le poste {title}\n\n"
            f"Bonjour,\n\n"
            f"Je souhaite candidater au poste de {title} au sein de {company}.\n"
            "Je suis particulièrement motivée par les sujets liés à l’IA, Azure, Databricks, la qualité des données et l’architecture Data.\n"
            "Je serais très heureuse de pouvoir échanger avec vous sur cette opportunité.\n"
            f"Lien vers l’annonce : {url}\n\n"
            "Cordialement,\nCynthia Sileu Kapnang"
        )

    def build_linkedin_message(self, job: Dict[str, object]) -> str:
        title = job.get("title", "poste")
        company = job.get("company", "votre entreprise")
        url = job.get("url", "")
        return (
            f"Bonjour,\n\n"
            f"Je suis très intéressée par le poste de {title} chez {company}.\n"
            "Mon profil s’aligne avec les enjeux Data, IA générative, Azure Databricks, RAG et gouvernance des données.\n"
            "Je serais ravie de discuter de cette opportunité.\n"
            f"Lien : {url}\n\n"
            "Cordialement,\nCynthia Sileu Kapnang"
        )
