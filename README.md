# 📚 Bibliothèque Municipale - API REST (Projet RAD)

Ce projet est le backend d'un système de gestion de bibliothèque municipale développé dans le cadre de l'évaluation de   RAD (Rapid Application Development)  . L'architecture a été conçue via une approche  Model-First  en utilisant le générateur de code *Telosys*, propulsée par *FastAPI* et hébergée en mode Serverless sur *Vercel* avec une base de données *PostgreSQL* sur *Render*.

🔗 *URL de l'API (Production):   [https://bibliotheque-rad.vercel.app](https://bibliotheque-rad.vercel.app)  
📖   Documentation Swagger :   [https://bibliotheque-rad.vercel.app/docs](https://bibliotheque-rad.vercel.app/docs)

---

## 🏗️ Architecture et Arborescence du Projet

L'arborescence a été pensée pour séparer la configuration Serverless (Vercel), la logique métier (src) et la modélisation (TelosysTools).

```text
bibliotheque-rad/
├── api/
│   └── index.py               # Point d'entrée Serverless pour Vercel
├── src/
│   ├── main.py                # Définition de l'application FastAPI et des routes
│   ├── database.py            # Configuration SQLAlchemy et connexion DB
│   ├── models.py              # Modèles ORM générés
│   └── schemas.py             # Schémas Pydantic (Validation des données, ex: ISBN)
├── TelosysTools/
│   ├── models/
│   │   └── LibraryModel/      # Fichiers DSL (.entity) définissant le domaine
│   └── telosys.cfg            # Configuration globale Telosys
├── .env                       # Variables d'environnement (ignoré par Git)
├── .gitignore                 # Fichiers à ignorer (venv, .env, __pycache__)
├── requirements.txt           # Dépendances du projet (FastAPI, psycopg2-binary...)
├── vercel.json                # Fichier de configuration du déploiement Vercel
└── README.md                  # Documentation du projet

Phase 1 : Initialisation et Dépôt Git

Plutôt que de cloner un projet existant, j'ai initialisé le projet de zéro :
# 1. Création du dossier et de l'environnement virtuel
mkdir bibliotheque-rad && cd bibliotheque-rad
python -m venv venv
venv\Scripts\activate  # (Sous Windows)

# 2. Initialisation de Git
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin [https://github.com/Codorah/bibliotheque-rad.git](https://github.com/Codorah/bibliotheque-rad.git)
git push -u origin main

Phase 2 : Modélisation avec Telosys (RAD)

Pour accélérer le développement, le modèle de données a été conçu avec le CLI Telosys

# Lancement de Telosys CLI
telosys
# Configuration du répertoire de travail et initialisation
h .
m librarymodel
init

J'ai ensuite défini trois entités principales dans mes fichiers DSL :

    Book.entity : Gestion des livres (avec contrainte d'unicité sur l'ISBN).

    Member.entity : Gestion des adhérents (avec email unique).

    Loan.entity : Table pivot gérant les dates d'emprunt et de retour.

    📸 Capture Telosys : Traces de la génération du modèle.
    (Insérer ici l'image telosys.png)


Phase 3 : Développement Backend (FastAPI)

    Dépendances : Installation des paquets requis via pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic.

    Base de données : Utilisation de SQLAlchemy pour se connecter à l'instance PostgreSQL.

    Validation : Utilisation de Pydantic pour valider les requêtes entrantes (notamment le format des ISBN).

Phase 4 : Exécution en Local

Pour tester l'API sur la machine de développement :

# Installation des dépendances
pip install -r requirements.txt

# Création du fichier .env
echo DATABASE_URL=postgresql://user:password@localhost/dbname > .env

# Lancement du serveur
uvicorn api.index:app --reload

L'interface locale est alors accessible sur http://127.0.0.1:8000/docs.
Phase 5 : Déploiement Cloud (Vercel & Render)

L'architecture de production est distribuée :

    Base de données (Render) : Hébergement gratuit d'une base PostgreSQL. J'ai récupéré l'External Database URL pour permettre les connexions entrantes.

    API (Vercel) : Déploiement du code via GitHub.

        Configuration du fichier vercel.json pour router le trafic vers api/index.py.

        Ajout de la variable DATABASE_URL dans les Settings de Vercel.

📊 Modélisation et Schémas
1. Diagramme de Classe UML (Domaine)

Ce diagramme illustre la structure métier du projet. Un adhérent peut avoir plusieurs emprunts, et chaque emprunt est lié à un livre spécifique.

(Insérer ici l'image diagramme.png)
2. Schéma de la Base de Données (PostgreSQL)

Le modèle physique généré dans la base de données reflète les contraintes de notre application :

    Table books : id (PK), title, author, isbn (UNIQUE), publication_year, available_copies.

    Table members : id (PK), name, email (UNIQUE), membership_date.

    Table loans : id (PK), book_id (FK -> books.id), member_id (FK -> members.id), loan_date, return_date.

📌 Tests et Validation de l'API

L'API expose un CRUD complet pour chaque entité. La documentation Swagger générée automatiquement permet de tester ces routes.

Exemples de points de terminaison :

    GET /books/ : Lister tous les livres.

    POST /books/ : Ajouter un nouveau livre (Valide que l'ISBN n'existe pas déjà).

    POST /loans/ : Créer un nouvel emprunt (Vérifie la disponibilité du livre).

📸 Capture Swagger : Test réussi de l'interface en production.(swagger.png)
