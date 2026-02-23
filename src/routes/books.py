from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src import schemas
from src.database import get_db
from src.models.models import Book, Loan

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    existing = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing:
        raise HTTPException(status_code=400, detail="ISBN already exists")

    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=list[schemas.BookRead])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Book).offset(skip).limit(limit).all()


@router.get("/{book_id}", response_model=schemas.BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.BookRead)
def update_book(book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    updates = payload.model_dump(exclude_unset=True)
    if "isbn" in updates and updates["isbn"] != book.isbn:
        existing = db.query(Book).filter(Book.isbn == updates["isbn"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="ISBN already exists")

    for key, value in updates.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    active_loan = (
        db.query(Loan)
        .filter(Loan.book_id == book_id)
        .filter(Loan.return_date.is_(None))
        .first()
    )
    if active_loan:
        raise HTTPException(status_code=400, detail="Book has active loans")

    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
