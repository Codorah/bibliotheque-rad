from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.database import Base, SessionLocal, engine
from src.models.models import Book, Loan, Member
from src.routes.books import router as books_router
from src.routes.loans import router as loans_router
from src.routes.members import router as members_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion Bibliotheque Municipale")
STATIC_DIR = Path(__file__).parent / "static"
FRONTEND_FILE = STATIC_DIR / "index.html"

app.include_router(books_router)
app.include_router(members_router)
app.include_router(loans_router)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def seed_demo_data() -> dict[str, int]:
    db = SessionLocal()
    created_books = 0
    created_members = 0
    created_loans = 0
    try:
        if db.query(Book).first() is None:
            books = [
                Book(
                    title="Le Petit Prince",
                    author="Antoine de Saint-Exupery",
                    isbn="9782070612758",
                    publication_year=1943,
                    available_copies=3,
                ),
                Book(
                    title="L Etranger",
                    author="Albert Camus",
                    isbn="9782070360024",
                    publication_year=1942,
                    available_copies=2,
                ),
                Book(
                    title="1984",
                    author="George Orwell",
                    isbn="9780451524935",
                    publication_year=1949,
                    available_copies=4,
                ),
            ]
            db.add_all(books)
            created_books = len(books)

        if db.query(Member).first() is None:
            members = [
                Member(name="Alice Benali", email="alice.benali@example.com"),
                Member(name="Karim Naciri", email="karim.naciri@example.com"),
            ]
            db.add_all(members)
            created_members = len(members)

        if created_books or created_members:
            db.commit()

        if db.query(Loan).first() is None:
            book = db.query(Book).filter(Book.available_copies > 0).first()
            member = db.query(Member).first()
            if book and member:
                loan = Loan(
                    book_id=book.id,
                    member_id=member.id,
                    loan_date=date.today(),
                    return_date=None,
                )
                book.available_copies -= 1
                db.add(loan)
                created_loans = 1
                db.commit()

        return {
            "books": created_books,
            "members": created_members,
            "loans": created_loans,
        }
    finally:
        db.close()


seed_demo_data()


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de la Bibliotheque"}


@app.get("/app")
def frontend():
    if not FRONTEND_FILE.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(FRONTEND_FILE)


@app.post("/seed-demo")
def seed_demo():
    created = seed_demo_data()
    return {"status": "ok", "created": created}


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
