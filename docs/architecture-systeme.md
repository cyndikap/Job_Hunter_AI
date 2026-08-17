# Architecture complète du système

## 1. Vue d'ensemble

Le système Job Hunter AI est un assistant de veille intelligente pour détecter automatiquement les offres d'emploi correspondant au profil d'un candidat Data / IA / Cloud. Il combine :

- collecte automatisée des offres,
- normalisation et déduplication,
- extraction de compétences,
- scoring de matching avec le CV,
- classification des opportunités,
- génération de contenu d'application,
- notification multi-canaux.

Le système est conçu pour être :

- fiable et évolutif,
- modulable par source de données,
- piloté par des agents IA spécialisés,
- compatible avec un déploiement Azure et un usage local via Docker.

## 2. Architecture technique

### 2.1 Couches fonctionnelles

1. Couche d'entrée / sources
   - LinkedIn Jobs
   - Welcome to the Jungle
   - APEC
   - HelloWork
   - Indeed
   - France Travail
   - LesJeudis
   - ChooseYourBoss
   - Jobteaser
   - Sites carrières des entreprises prioritaires

2. Couche d'ingestion
   - scraping / API adapters / parsers HTML
   - normalisation des champs : entreprise, poste, lieu, type de contrat, salaire, compétences, description, lien
   - déduplication par signature stable (titre + entreprise + URL + date)

3. Couche IA
   - extraction de compétences
   - scoring de matching
   - résumé automatique du poste
   - comparaison avec le CV
   - génération d'email, message LinkedIn et lettre de motivation

4. Couche d'orchestration
   - API backend FastAPI
   - scheduler APScheduler / Airflow
   - workers de traitement asynchrones
   - file de tâches (optionnel : Celery/RQ)

5. Couche de sortie
   - dashboard Streamlit
   - alertes email / Teams / Discord / Telegram
   - historique des candidatures
   - tableau de suivi

## 3. Composants principaux

### Frontend - Streamlit

Le frontend permet de :

- consulter les jobs détectés,
- filtrer par score, source et statut,
- visualiser les compétences détectées,
- suivre le pipeline de candidatures,
- suivre les alertes et avis de matching,
- lancer des tâches manuelles de re-scan.

### Backend - FastAPI

Responsibilities :

- API REST pour la gestion des offres et du suivi,
- endpoint de re-scan,
- endpoint de génération de messages,
- endpoints de santé et monitoring,
- orchestration des tâches IA et de notification.

### Orchestrateur de tâches

- APScheduler pour exécuter toutes les heures un job de collecte
- Airflow pour planification avancée et dépendances si besoin d'échelle

### IA / LLM

- Azure OpenAI comme moteur principal
- Modèle recommandé : GPT-4o ou GPT-4.1-mini selon budget
- Utilisation : extraction de compétences, classification, résumé, email/motivation

### Base de données

- PostgreSQL pour les données transactionnelles et le suivi
- stockage de : jobs, compétences, profils, matching, candidatures, notifications

### Monitoring

- Grafana + Prometheus / Loki
- métriques : jobs collectés, taux de matching, temps de traitement, erreurs par source

## 4. Agents IA nécessaires

### Agent 1 - Job Discovery Agent

Rôle :

- consulte les sources de jobs,
- récupère les nouvelles offres,
- extrait les structures de données,
- envoie les offres normalisées à l'étape suivante.

### Agent 2 - Skill Extraction Agent

Rôle :

- lit la description de poste,
- détecte les compétences clés,
- compare avec le profil candidat,
- ressort les points forts et manquants.

### Agent 3 - Matching Agent

Rôle :

- calcule le score global de matching,
- compare le rôle recherché, les compétences, la localisation, l'expérience,
- attribue une catégorie d'adéquation : très forte / forte / moyenne / faible.

### Agent 4 - Summary Agent

Rôle :

- résume le poste en 4 à 6 lignes,
- liste les compétences détectées,
- met en avant les éléments clés de l'offre.

### Agent 5 - Outreach Agent

Rôle :

- génère un email personnalisé,
- un message LinkedIn au recruteur,
- une lettre de motivation adaptée,
- une version courte/longue selon le contexte.

### Agent 6 - Notification Agent

Rôle :

- envoie les alertes par email, Teams, Discord, Telegram,
- respecte le seuil de notification,
- centralise les messages d'alerte et la logique d'envoi.

### Agent 7 - Ops Monitor Agent

Rôle :

- surveille le pipeline,
- détecte les échecs de scraping,
- signale les sources non fiables,
- alerte sur les ratios de matching anormaux.

## 5. Modèle de scoring

### 5.1 Poids recommandés

- Titre du poste / rôle : 25%
- Compétences techniques : 30%
- Expérience / contexte : 15%
- Cloud / Azure / Databricks : 10%
- Data Governance / MDM / AI / RAG / LLM : 10%
- Type de contrat / localisation / télétravail : 5%
- Entreprise prioritaire / secteur : 5%

### 5.2 Compétences qui augmentent fortement le score

- Azure Databricks
- Azure
- Python
- SQL
- RAG
- LLM
- Azure OpenAI
- Agentic AI
- MLflow
- MLOps
- FastAPI
- Data Governance
- MDM
- PIM
- Snowflake

### 5.3 Seuils de classification

- 90-100 : Très forte adéquation
- 80-89 : Forte adéquation
- 70-79 : Adéquation moyenne
- < 70 : Ne pas notifier

## 6. Règles de filtrage métier

- besoins de localisation : France / Île-de-France
- type de contrat : CDI
- télétravail partiel ou complet accepté
- rôle orienté Data / IA / Cloud
- exclusion des offres non pertinentes ou trop éloignées du profil

## 7. Flux de données

Le flux de données principal est le suivant :

1. Collecte des offres depuis les sources
2. Nettoyage et normalisation
3. Déduplication
4. Stockage dans PostgreSQL
5. Extraction des compétences par LLM
6. Matching avec le profil candidat
7. Scoring et classification
8. Génération des alertes et messages
9. Suivi historique dans le CRM interne

## 8. Sécurité et conformité

- stockage des secrets dans Azure Key Vault ou variables d’environnement sécurisées,
- masquage des données sensibles dans les logs,
- conformité RGPD pour les données de candidature,
- limites de rate limit sur les sources web,
- respect des conditions d’utilisation des plateformes de recrutement.

## 9. Évolutivité

Le système peut évoluer vers :

- plus de sources de jobs,
- plus de canaux de notification,
- un moteur de ranking plus intelligent,
- des agents multi-candidats,
- intégration CRM / ATS,
- prévisions et analytics sur les tendances du marché.

## 10. Architecture cible recommandée

Le design cible idéal est le suivant :

- Streamlit pour le front-office
- FastAPI pour l’API backend
- PostgreSQL pour le stockage relationnel
- APScheduler pour le planificateur principal
- Azure OpenAI pour les tâches de raisonnement IA
- Docker pour l’environnement d’exécution
- Grafana pour la surveillance
- Redis (optionnel) pour les files de jobs asynchrones
