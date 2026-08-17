MATCHING_PROMPT = """
Tu es un expert en recrutement tech Data, IA et Cloud. 
Analyse l’offre ci-dessous et compare-la au profil candidat suivant :

Profil candidat :
- AI & Data Engineer
- Data Engineering
- Generative AI
- Agentic AI
- RAG
- LLM
- Azure Databricks
- Azure
- Python
- SQL
- Data Governance
- MDM
- FastAPI
- MLflow
- Azure OpenAI

Offre :
{job_description}

Retourne un JSON strict avec :
- score: nombre entre 0 et 100
- classification: très forte adéquation / forte adéquation / adéquation moyenne / à revoir
- matched_skills: liste des compétences communes
- strengths: points forts de compatibilité
- missing_skills: compétences manquantes
- summary: résumé de 4 lignes du poste
"""

SUMMARY_PROMPT = """
Rédige un court résumé en français du poste et mets en avant :
- mission principale
- compétences attendues
- contexte technique
- points clés de l’offre

 Poste : {title}
 Entreprise : {company}
 Description : {description}
"""

EMAIL_PROMPT = """
Rédige un email professionnel et personnalisé à destination du recruteur pour une candidature en français.
Inclure :
- objectif de candidature
- lien avec le poste
- profil Data / IA / Azure
- motivation
- appel à un échange

 Poste : {title}
 Entreprise : {company}
 Profil : {candidate_profile}
"""

LINKEDIN_PROMPT = """
Rédige un message LinkedIn professionnel concis pour un recruteur en français.
Le message doit :
- être clair
- montrer une forte adéquation avec le poste
- noter les compétences clés
- inviter au contact

 Poste : {title}
 Entreprise : {company}
 Niveau de match : {score}%
"""
