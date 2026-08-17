# Plan d'implémentation détaillé

## 1. Objectif de l'implémentation

Mise en place d’un premier système exploitable en 7 jours, avec une base solide pour évoluer vers un produit de veille recrutement intelligent et industrialisable.

## 2. MVP réalisable en 1 semaine

### Phase 1 – Analyse et cadrage (Jour 1)

- validation du profil candidat et des offres cibles,
- définition des sources prioritaires,
- finalisation des règles de matching,
- création du schéma PostgreSQL,
- définition des seuils de notification.

### Phase 2 – Fondations techniques (Jour 2)

- initialisation du repo,
- création de l’API FastAPI,
- mise en place de la base PostgreSQL,
- configuration Docker,
- intégration Azure OpenAI,
- mise en place du dashboard Streamlit.

### Phase 3 – Collecte et normalisation (Jour 3)

- intégration des sites prioritaires : LinkedIn Jobs, WTTJ, APEC, Indeed,
- scrapers / parsers / adaptateurs,
- extraction des champs principaux,
- création de la logique de déduplication.

### Phase 4 – Matching IA (Jour 4)

- extraction de compétences de l’offre,
- extraction de compétences du CV,
- calcul de score pondéré,
- génération de résumé de poste,
- classification en 4 niveaux.

### Phase 5 – Alertes et suivi (Jour 5)

- génération d’email personnalisé,
- notification Teams / Discord / Telegram,
- création du tableau de suivi des candidatures,
- ajout du statut de traitement pour chaque offre.

### Phase 6 – Validation et correctifs (Jour 6)

- test de vraies offres sur un périmètre limité,
- amélioration du score,
- correction des faux positifs,
- test des canaux de notification.

### Phase 7 – Livraison (Jour 7)

- mise en prod locale ou sur Azure,
- vérification du flux complet de bout en bout,
- demonstration du dashboard et des alertes,
- documentation utilisateur.

## 3. Version avancée industrialisable

### Architecture cible

- orchestration robuste sur Airflow ou APScheduler avec workers,
- qualité de données et monitoring,
- sources étendues à plus de 10 channels,
- collecte multi-plateforme en temps réel,
- ranking multi-critères plus avancé,
- pipeline complet de préparation à la candidature.

### Capacités avancées

- moteur de ranking hybride : règles + IA,
- historique et apprentissage du comportement utilisateur,
- analyse des tendances marché,
- monitoring par source et par entreprise,
- intégration CRM / ATS / email drafting,
- réaction automatique sur nouvelles offres.

## 4. Plan de production

### Environnement de dev

- Docker Compose local
- PostgreSQL local
- Streamlit local
- FastAPI local
- Azure OpenAI en mode test

### Environnement de prod

- conteneurs Docker sur un VM ou Azure Container Apps,
- PostgreSQL managé,
- secret management via Azure Key Vault,
- observabilité via Grafana,
- exécution automatique via scheduler.

## 5. Roadmap recommandée

### Sprint 1 – MVP

- sources : 4 sources prioritaires
- alertes : email + Teams
- scoring et classement
- tableau de suivi

### Sprint 2 – Intelligence

- enrichissement IA des offres
- résumé automatique
- génération d’email personnalisé
- amélioration du score

### Sprint 3 – Industrialisation

- monitoring et alerting technique
- gestion de la qualité des sources
- support multi-canaux et multi-profil
- orchestrations avancées

## 6. KPIs à suivre

- nombre d’offres collectées / jour,
- taux de déduplication,
- taux de matching > 80%,
- taux de faux positifs,
- temps de traitement moyen,
- volume de notifications envoyées,
- taux de candidature réelle,
- temps entre publication et notification.

## 7. Critères de réussite

- le système détecte des offres pertinentes sans bruit excessif,
- les offres maintiennent un score cohérent avec le profil,
- l'alerte est transmise en moins de 30 minutes après publication,
- le dashboard permet un suivi simple et exploitable,
- l’utilisateur reçoit un niveau de qualité suffisant pour agir rapidement.
