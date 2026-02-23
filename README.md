# Systeme de Gestion de Bibliotheque Municipale

Backend FastAPI pour la gestion des livres, adherents et emprunts, avec modelisation Telosys et persistance PostgreSQL.

## Livrables Examen (Checklist)

- [x] Code backend FastAPI (`src/`)
- [x] Dossier modeles SQLAlchemy (`src/models/`)
- [x] Dossier routes API (`src/routes/`)
- [x] Fichiers DSL Telosys (`TelosysTools/models/LibraryModel/*.entity`)
- [x] `requirements.txt`
- [x] `README.md` documente
- [x] telosys.png (processus telosys)
- [x] diagramme.png(diagramme plantuml)
- [x] https://github.com/Codorah/bibliotheque-rad.git
- [ ] Lien API deployee

## Structure

```txt
.
|-- api/
|   `-- index.py
|-- src/
|   |-- database.py
|   |-- main.py
|   |-- schemas.py
|   |-- models/
|   |   |-- __init__.py
|   |   `-- models.py
|   |-- static/
|   |   `-- index.html
|   `-- routes/
|       |-- __init__.py
|       |-- books.py
|       |-- members.py
|       `-- loans.py
|-- TelosysTools/
|   `-- models/
|       `-- LibraryModel/
|           |-- Book.entity
|           |-- Member.entity
|           `-- Loan.entity
|-- requirements.txt
`-- vercel.json
```

## Entites du Domaine

- `Book`: `id`, `title`, `author`, `isbn`, `publication_year`, `available_copies`
- `Member`: `id`, `name`, `email`, `membership_date`
- `Loan`: `id`, `book_id`, `member_id`, `loan_date`, `return_date`

## Telosys (CLI)

Dans le terminal `telosys>`:

```txt
h .
init
nm LibraryModel
m LibraryModel
ne Book
ne Member
ne Loan
```

Fichiers DSL utilises:

- `TelosysTools/models/LibraryModel/Book.entity`
- `TelosysTools/models/LibraryModel/Member.entity`
- `TelosysTools/models/LibraryModel/Loan.entity`

## Installation Locale

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration Environnement

Copier `.env.example` vers `.env`:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/library_db
```

## Lancer l'API

```bash
uvicorn src.main:app --reload
```

Swagger:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`
- Frontend mini dashboard: `http://127.0.0.1:8000/app`

## API CRUD (minimum)

### Book

- `POST /books/`
- `GET /books/`
- `GET /books/{book_id}`
- `PUT /books/{book_id}`
- `DELETE /books/{book_id}`

### Member

- `POST /members/`
- `GET /members/`
- `GET /members/{member_id}`
- `PUT /members/{member_id}`
- `DELETE /members/{member_id}`

### Loan

- `POST /loans/`
- `GET /loans/`
- `GET /loans/{loan_id}`
- `PUT /loans/{loan_id}`
- `PUT /loans/{loan_id}/return`
- `DELETE /loans/{loan_id}`
- `POST /seed-demo` (alimente des donnees de demonstration si la base est vide)

## Regles de Validation

- ISBN unique pour `Book`.
- Email unique pour `Member`.
- Un pret (`Loan`) ne peut etre cree que si:
  - le livre existe,
  - l'adherent existe,
  - `available_copies > 0`.

## Diagramme UML

```mermaid
classDiagram
  class Book {
    +int id
    +string title
    +string author
    +string isbn
    +int publication_year
    +int available_copies
  }

  class Member {
    +int id
    +string name
    +string email
    +date membership_date
  }

  class Loan {
    +int id
    +int book_id
    +int member_id
    +date loan_date
    +date return_date
  }

  Book "1" --> "0..*" Loan : has
  Member "1" --> "0..*" Loan : makes
```

## Schema BD (ER)

```mermaid
erDiagram
  BOOKS ||--o{ LOANS : has
  MEMBERS ||--o{ LOANS : makes

  BOOKS {
    int id PK
    string title
    string author
    string isbn UK
    int publication_year
    int available_copies
  }

  MEMBERS {
    int id PK
    string name
    string email UK
    date membership_date
  }

  LOANS {
    int id PK
    int book_id FK
    int member_id FK
    date loan_date
    date return_date
  }
```

## Captures d'Ecran Telosys (a inserer)

Inserer des captures:

1. `Telosys: Init project`
2. `Telosys: New model` (`LibraryModel`)
3. Creation de `Book.entity`, `Member.entity`, `Loan.entity`
4. Telechargement bundle
5. Generation de code

## Deploiement sur Vercel 

1. Pousser le code sur GitHub (repo public).
2. Creer une base PostgreSQL  Render 
3. Importer le repo dans Vercel.
4. Garder `vercel.json` du projet (route tout vers `api/index.py`).
5. Ajouter la variable d'environnement `DATABASE_URL` dans Vercel.
6. Deploy et tester:
   - `https://<ton-projet>.vercel.app/docs`
   - `https://<ton-projet>.vercel.app/health`

## Commandes GitHub Push

```bash
git init
git add .
git commit -m "Backend FastAPI + Telosys + Vercel config"
git branch -M main
git remote add origin https://github.com/Codorah/bibliotheque-rad.git
git push -u origin main
```
