Agis comme un Architecte Logiciel Senior, Product Owner, Expert IA, Expert Python, Expert Next.js et Expert Automation.

Je souhaite construire une application nommée "Job Hunter AI".

Contexte
Job Hunter AI est un agent intelligent de veille emploi destiné aux profils Data, IA, Cloud, Engineering et Produit Digital.

L'objectif principal est de détecter les nouvelles offres d'emploi le plus rapidement possible après leur publication (objectif : moins de 30 minutes après publication).

L'application doit surveiller plusieurs plateformes d'emploi et notifier automatiquement l'utilisateur lorsqu'une nouvelle opportunité pertinente apparaît.

Cette application ne doit dépendre d'aucun outil interne Capgemini.

Le projet doit être totalement indépendant et déployable sur un compte personnel.

Sources à surveiller
L'application doit surveiller :

LinkedIn Jobs
Welcome to the Jungle
Hellowork
APEC
Indeed
LesJeudis
Sites carrières d'entreprises
La surveillance doit être effectuée automatiquement toutes les 5 à 10 minutes.

Fonctionnalités principales
1. Collecte des offres
Créer un moteur de collecte capable de :

détecter les nouvelles offres
éviter les doublons
récupérer :
titre du poste
entreprise
localisation
date de publication
description
compétences demandées
url de l'offre
Utiliser :

Playwright
Apify (si pertinent)
2. Analyse du profil candidat
Créer un profil utilisateur contenant :

nom
email
CV
compétences
expériences
localisation souhaitée
niveau d'expérience
Exemple de compétences :

Azure
Databricks
PySpark
Python
SQL
Data Engineering
Machine Learning
GenAI
Spark
DevOps
3. Matching IA
Créer un moteur IA capable de comparer :

CV utilisateur
VS
Description de poste

Calculer :

score global (/100)
score compétences
score expérience
score localisation
Classifier :

Excellent Match
Strong Match
Moderate Match
Weak Match
Utiliser :

Ollama
Mistral
Embeddings
Qdrant
4. Détection temps réel
Créer un scheduler automatique.

Objectif :

scan toutes les 5 minutes
identifier uniquement les nouvelles offres
enregistrer la date de première détection
Mesurer :

heure publication
heure détection
temps de réaction
Afficher un KPI :

"Temps moyen de détection"

Objectif :
< 30 minutes

5. Alertes email
Quand une offre dépasse 80% de compatibilité :

envoyer automatiquement un email.

Contenu :

titre
entreprise
score
compétences communes
date de publication
bouton "Voir l'offre"
Utiliser :

Brevo
6. Génération de messages recruteur
Créer un moteur IA générant :

message LinkedIn
email de candidature
email de relance
Prendre en compte :

entreprise
poste
CV utilisateur
expérience utilisateur
Chaque message doit être personnalisé.

7. Recherche recruteur
Lorsque disponible :

extraire :

nom du recruteur
fonction
email
profil LinkedIn
Associer les informations à l'offre.

8. CRM de candidatures
Créer un système de suivi des candidatures.

Statuts :

Détectée
À analyser
À postuler
Candidature envoyée
Contact recruteur envoyé
Relance envoyée
Entretien RH
Entretien technique
Offre reçue
Refusée
Acceptée
Historiser chaque changement.

9. Dashboard
Créer un dashboard moderne.

Afficher :

nombre d'offres détectées
nombre d'offres pertinentes
nombre d'offres postulées
nombre de réponses
taux de conversion
temps moyen de détection
Widgets :

nouvelles offres
meilleures opportunités
alertes
statistiques
10. Recherche intelligente
Ajouter :

filtres
recherche sémantique
moteur de recommandation
Permettre :

localisation
télétravail
entreprise
salaire
technologies
Architecture technique
Frontend :

Next.js
React
Tailwind
TypeScript
Backend :

FastAPI
Base de données :

PostgreSQL
Supabase
Vector Database :

Qdrant
IA :

Ollama
Mistral
Notifications :

Brevo
Déploiement :

Vercel
Railway
Livrables attendus
Produis :

Architecture complète
Diagramme d'architecture
Structure des dossiers
Modèle de données SQL
Schéma Supabase
APIs FastAPI
Modèles Pydantic
Interface utilisateur Next.js
Workflow de surveillance
Workflow de matching IA
Workflow d'envoi d'emails
Plan de déploiement
Roadmap MVP puis V2
Code complet fichier par fichier
Tests unitaires
Tests d'intégration
Docker Compose complet
L'application doit être prête pour une utilisation réelle et capable de surveiller les offres d'emploi en continu.