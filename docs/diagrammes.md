# Diagrammes du système

## 1. Diagramme des composants

```mermaid
flowchart LR
    A[Sources de jobs\nLinkedIn / WTTJ / APEC / Indeed / etc.] --> B[Job Collectors]
    B --> C[Normalizer + Deduplicator]
    C --> D[(PostgreSQL)]
    D --> E[Matching Engine]
    E --> F[Skill Extraction Agent]
    F --> G[Scoring & Classification]
    G --> H[Notification Agent]
    G --> I[Outreach Agent]
    G --> J[Streamlit Dashboard]
    H --> K[Email]
    H --> L[Teams]
    H --> M[Discord]
    H --> N[Telegram]
    E --> O[Azure OpenAI]
    J --> P[User / Candidate]
    D --> Q[Application Tracker]
    Q --> J
```

## 2. Diagramme de flux de données

```mermaid
sequenceDiagram
    participant Src as Sources de jobs
    participant Col as Collector
    participant Norm as Normalizer
    participant DB as PostgreSQL
    participant AI as Azure OpenAI
    participant Match as Matching Engine
    participant Notif as Notification Service
    participant UI as Streamlit

    Src->>Col: Nouvelles offres
    Col->>Norm: Données brutes
    Norm->>DB: Offres normalisées
    DB->>Match: Récupération des offres
    Match->>AI: Extraction des compétences + résumé
    AI-->>Match: Compétences / résumé / points forts
    Match->>DB: Score + classification + forces / manquants
    Match->>Notif: Offres candidates
    Notif->>UI: Alertes + recommandations
    UI->>User: Dashboard + notifications
```

## 3. Diagramme d’architecture applicative

```mermaid
flowchart TD
    subgraph Frontend
        UI[Streamlit Dashboard]
    end

    subgraph Backend
        API[FastAPI API]
        SCHED[APScheduler / Airflow]
        WORKER[Workers Jobs]
        MATCH[Scoring Engine]
        OUT[Outreach Generator]
    end

    subgraph AI
        LLM[Azure OpenAI]
    end

    subgraph Data
        PG[(PostgreSQL)]
        RAW[Raw Job Storage]
    end

    subgraph Ops
        GRAF[Grafana]
        MON[Monitoring / Logs]
    end

    UI --> API
    SCHED --> WORKER
    WORKER --> MATCH
    MATCH --> LLM
    MATCH --> PG
    OUT --> LLM
    API --> PG
    UI --> PG
    PG --> GRAF
    MON --> GRAF
```

## 4. Diagramme de logique de score

```mermaid
flowchart TD
    A[CV + profil candidat] --> B[Profil skills model]
    C[Offre] --> D[Extraction skills] 
    B --> E[Similarity engine]
    D --> E
    E --> F[Score global]
    F --> G{Seuil}
    G -->|>= 90| H[Très forte adéquation]
    G -->|80-89| I[Forte adéquation]
    G -->|70-79| J[Adéquation moyenne]
    G -->|< 70| K[Ignorer]
```

## 5. Diagramme de notification

```mermaid
flowchart LR
    A[Offre qualifiée] --> B[Notification Agent]
    B --> C[Email]
    B --> D[Teams]
    B --> E[Discord]
    B --> F[Telegram]
    B --> G[Dashboard / historique]
```
