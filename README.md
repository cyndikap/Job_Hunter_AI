# Job Hunter AI

Agent IA personnel de veille emploi spécialisé Data, IA, Cloud et Azure.

## Objectif

Détecter, filtrer, noter et notifier automatiquement les offres d'emploi correspondant au profil de Cynthia Sileu Kapnang : AI & Data Engineer, avec un focus sur Azure, Databricks, IA générative, agentic AI, RAG et data governance.

## Profil cible

- AI & Data Engineer
- Data Engineering / Generative AI / Agentic AI / RAG / LLM
- Azure Databricks, Azure OpenAI, Python, SQL, MDM, Data Governance
- Recherche : CDI, Île-de-France, télétravail partiel/complet, France

## Livrables

- [docs/architecture-systeme.md](docs/architecture-systeme.md)
- [docs/diagrammes.md](docs/diagrammes.md)
- [docs/plan-implementation.md](docs/plan-implementation.md)
- [docs/schema-bdd.sql](docs/schema-bdd.sql)

## Vue d'ensemble

Le système collecte les offres depuis plusieurs sources, les normalise, les enrichit par IA, calcule un score de matching avec le CV, puis déclenche des alertes et prépare des éléments de candidature (résumé, email, message LinkedIn, lettre de motivation et suivi).

### Principales fonctionnalités

- Veille automatique toutes les heures
- Extraction de compétences à partir des offres et du CV
- Scoring de matching pondéré
- Déduplication des annonces
- Classification en forte / moyenne / faible adéquation
- Alertes multi-canaux : email, Teams, Discord, Telegram
- Génération d'outreach personnalisée
- Tableau de bord de suivi

## Architecture

Le projet suit une architecture modulaire en 5 couches :

1. Sources de données
2. Ingestion et normalisation
3. Analyse IA et matching
4. Orchestration et planification
5. Notifications et suivi candidat

## Stack technique recommandée

- Frontend : React + Vite
- Backend : FastAPI
- LLM : Azure OpenAI
- Base de données : PostgreSQL
- Planification : APScheduler ou Airflow
- Conteneurisation : Docker
- Monitoring : Grafana

## Démarrage rapide

1. Copier les variables d'environnement depuis le fichier de configuration fourni dans le dépôt.
2. Lancer la pile locale avec Docker Compose.
3. Démarrer l’API FastAPI.
4. Démarrer le dashboard React.
5. Vérifier la collecte et le scoring sur un jeu de données d’exemple.

## Portée MVP (1 semaine)

- 4 sources prioritaires
- calcul de matching robuste
- alertes email + Teams
- tableau de suivi minimal
- génération de résumé et d’email de candidature

## Version avancée

- collecte multi-sources complète
- agents IA spécialisés
- queue de traitement asynchrone
- personnalisation avancée du message
- monitoring, métriques, dashboard analytique

## Auteur

Cynthia Sileu Kapnang
