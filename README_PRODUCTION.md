# Job Hunter AI - Production

## 1. Objectif

Application SaaS de veille emploi, CRM de candidatures, IA conversationnelle et monitoring de performance de recherche d'emploi.

## 2. Architecture

- Frontend: React + Vite
- Backend: FastAPI
- Base de données: PostgreSQL / Supabase
- Vector DB: Qdrant
- IA: Ollama + Mistral fallback
- Email: SMTP + IMAP
- Déploiement: Railway + Vercel

```mermaid
flowchart LR
    U[Utilisateur] --> FE[Frontend Vercel]
    FE --> API[FastAPI Backend]
    API --> PG[(Supabase PostgreSQL)]
    API --> QDR[Qdrant Cloud]
    API --> LLM[Ollama / Mistral]
    API --> SMTP[SMTP / IMAP]
```

## 3. Variables d'environnement

### Backend
```env
APP_ENV=production
APP_NAME="Job Hunter AI"
APP_BASE_URL=https://app.your-domain.com
API_V1_PREFIX=/api/v1

JWT_SECRET=replace_with_strong_32_plus_char_secret
JWT_ALGORITHM=HS256
JWT_TTL_MINUTES=60

DATABASE_URL=postgresql://user:password@host:5432/dbname
DATABASE_ECHO=false

SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=xxxxx
SUPABASE_ANON_KEY=xxxxx

QDRANT_URL=https://xxxxx.qdrant.io
QDRANT_API_KEY=xxxxx
QDRANT_COLLECTION_NAME=jobhunter_vectors

OLLAMA_BASE_URL=http://internal-ollama-host:11434
OLLAMA_MODEL=llama3.2
OLLAMA_ENABLED=false

MISTRAL_API_KEY=xxxxx
MISTRAL_MODEL=mistral-small-latest
MISTRAL_ENABLED=true

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=no-reply@your-domain.com
SMTP_FROM_NAME="Job Hunter AI"

IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=your-email
IMAP_PASSWORD=your-app-password
IMAP_MAILBOX=INBOX

ALLOWED_ORIGINS=https://app.your-domain.com,https://www.your-domain.com
CORS_ALLOW_CREDENTIALS=true

LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=120
ADMIN_USER_IDS=user_id_1,user_id_2
```

### Frontend
```env
VITE_API_BASE_URL=https://api.your-domain.com
VITE_APP_NAME="Job Hunter AI"
```

## 4. Déploiement backend Railway

1. Créer un service backend sur Railway.
2. Connecter le dépôt GitHub.
3. Définir le dossier racine sur `backend`.
4. Définir la commande de démarrage :
```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```
5. Ajouter les variables d'environnement backend.
6. Vérifier `/health`.
7. Vérifier `/metrics`.

## 5. Déploiement frontend Vercel

1. Créer un projet Vercel.
2. Importer le repo frontend.
3. Définir la commande de build :
```bash
npm run build
```
4. Définir le dossier de sortie :
```bash
dist
```
5. Ajouter `VITE_API_BASE_URL`.
6. Configurer le domaine personnalisé.
7. Vérifier l'accès HTTPS.

## 6. Configuration Supabase production

- Créer le projet Supabase dédié à la production.
- Ajouter `DATABASE_URL` dans le backend.
- Activer les backups automatiques.
- Activer RLS et policies de sécurité.
- Vérifier que chaque table contient `user_id`.
- Tester l'isolation entre utilisateurs.

## 7. Configuration Qdrant Cloud

- Créer le cluster Qdrant Cloud.
- Ajouter `QDRANT_URL` et `QDRANT_API_KEY`.
- Vérifier la connectivité depuis le backend.
- Créer les collections vectorielles.
- Valider le filtrage par `user_id`.
- Vérifier la latence et la stabilité.

## 8. Checklist Go-Live

### Environnement
- [ ] Variables de production configurées
- [ ] JWT secret configuré
- [ ] SMTP configuré
- [ ] IMAP configuré
- [ ] Supabase production configuré
- [ ] Qdrant production configuré
- [ ] Domaine HTTPS défini

### Backend
- [ ] Railway backend déployé
- [ ] Commande de lancement valide
- [ ] `/health` OK
- [ ] `/metrics` OK
- [ ] API accessible via HTTPS
- [ ] Auth JWT OK
- [ ] Routes protégées sécurisées

### Frontend
- [ ] Vercel déployé
- [ ] `VITE_API_BASE_URL` configuré
- [ ] Build OK
- [ ] Login OK
- [ ] Dashboard OK
- [ ] AI Insights OK
- [ ] Admin OK

### Données et sécurité
- [ ] Supabase connecté
- [ ] RLS activé
- [ ] Isolation utilisateur validée
- [ ] Qdrant connecté
- [ ] Filtrage vecteur validé
- [ ] CORS restreint
- [ ] Rate limiting activé

### Validation fonctionnelle
- [ ] Signup OK
- [ ] Signin OK
- [ ] Scan jobs OK
- [ ] Matching OK
- [ ] Email alert OK
- [ ] CRM mis à jour
- [ ] Chat IA OK
- [ ] Isolation utilisateur OK

### Mise en production
- [ ] Monitoring activé
- [ ] Rollback prêt
- [ ] Smoke tests passés
- [ ] Go-live approuvé

## 9. Checklist Post-Go-Live

### Premières 24h
- [ ] Disponibilité API surveillée
- [ ] Taux d'erreur surveillé
- [ ] Échecs d'auth surveillés
- [ ] Latence LLM surveillée
- [ ] Latence Qdrant surveillée
- [ ] Erreurs SMTP surveillées
- [ ] Activité utilisateur suivie
- [ ] Incidents critiques revus
- [ ] Santé base de données revue

### Jours 2 à 7
- [ ] Usage dashboard stable
- [ ] Qualité chat IA revue
- [ ] Qualité matching revue
- [ ] Taux de succès alertes reviewé
- [ ] Utilisation CRM suivie
- [ ] Événements sécurité revus
- [ ] Tendances performance revue
- [ ] Retrospective de release effectuée

## 10. Checklist sécurité finale

- [ ] JWT secret unique et fort
- [ ] Aucune donnée sensible dans le dépôt
- [ ] Toutes les routes sensibles exigent une authentification
- [ ] Accès aux données filtré par `user_id`
- [ ] Requêtes RAG filtrées par utilisateur
- [ ] Accès admin limité aux comptes autorisés
- [ ] CORS limité aux domaines de confiance
- [ ] Rate limiting activé
- [ ] Logs sans secrets
- [ ] Credentials SMTP/IMAP en variables d'environnement uniquement
- [ ] RLS activé sur la base de données
- [ ] Isolation utilisateur validée
- [ ] Smoke tests prod passés
- [ ] Monitoring actif
- [ ] Plan de rollback prêt

## 11. Checklist validation E2E finale

### Authentification
- [ ] Signup OK
- [ ] Signin OK
- [ ] Token invalide rejeté
- [ ] Token expiré rejeté
- [ ] Restrictions admin vérifiées

### Workflow principal
- [ ] Dashboard chargé
- [ ] Scan des offres OK
- [ ] Score de matching calculé
- [ ] Génération d'alerte OK
- [ ] Envoi email OK
- [ ] Réponse recruteur traitée
- [ ] CRM mis à jour
- [ ] Dashboard rafraîchi

### Workflow IA
- [ ] Chat IA OK
- [ ] Contexte utilisateur utilisé
- [ ] Réponses limitées au scope utilisateur
- [ ] Pas de fuite inter-utilisateur

### Isolation
- [ ] User A ne voit pas les données User B
- [ ] User A ne voit pas l'historique User B
- [ ] User A ne voit pas les analytics User B
- [ ] User A ne voit pas les vecteurs User B

### Production readiness
- [ ] Backend healthy
- [ ] Frontend healthy
- [ ] Connectivité API OK
- [ ] Monitoring actif
- [ ] Rollback prêt
- [ ] Lancement approuvé

## 12. Procédure de mise en production

1. Valider toutes les variables d'environnement.
2. Vérifier le backend Railway.
3. Vérifier le frontend Vercel.
4. Vérifier Supabase et Qdrant.
5. Vérifier auth et données utilisateur.
6. Lancer les tests E2E.
7. Vérifier monitoring et logs.
8.Valider le flux complet utilisateur.
9. Déclencher la mise en production.

## 13. Procédure de rollback

1. Revenir sur la dernière version stable.
2. Redéployer le backend stable.
3. Redéployer le frontend stable.
4. Vérifier les variables d'environnement.
5. Vérifier la base de données.
6. Vérifier la santé de l'application.
7. Refaire un smoke test.
8. Analyser la cause racine avant un nouveau déploiement.

## 14. Monitoring de production

- `/health`
- `/metrics`
- logs backend
- logs frontend
- connectivité DB
- connectivité Qdrant
- connectivité SMTP/IMAP

## 15. Critères de Go-Live

- [ ] production env complète
- [ ] backend en ligne
- [ ] frontend en ligne
- [ ] Supabase en ligne
- [ ] Qdrant en ligne
- [ ] auth validée
- [ ] isolation validée
- [ ] tests E2E passés
- [ ] monitoring activé
- [ ] rollback prêt

## 16. Notes opérationnelles

- Séparer strictement environnement de développement et de production.
- Faire des backups réguliers.
- Rotation des secrets à planifier.
- Conserver un canal de revue d'incidents.
- Garder une release rollbackable et documentée.
