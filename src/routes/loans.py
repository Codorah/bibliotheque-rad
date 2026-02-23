from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src import schemas
from src.database import get_db
from src.models.models import Book, Loan, Member

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=schemas.LoanRead, status_code=status.HTTP_201_CREATED)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No available copies")

    member = db.query(Member).filter(Member.id == loan.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db_loan = Loan(**loan.model_dump())
    book.available_copies -= 1

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


@router.get("/", response_model=list[schemas.LoanRead])
def list_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Loan).offset(skip).limit(limit).all()


@router.get("/{loan_id}", response_model=schemas.LoanRead)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.put("/{loan_id}", response_model=schemas.LoanRead)
def update_loan(loan_id: int, payload: schemas.LoanUpdate, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return loan

    if "loan_date" in updates:
        loan.loan_date = updates["loan_date"]

    if "return_date" in updates:
        previous_return_date = loan.return_date
        new_return_date = updates["return_date"]

        if previous_return_date is None and new_return_date is not None:
            # Returning an active loan frees one copy.
            book = db.query(Book).filter(Book.id == loan.book_id).first()
            if book:
                book.available_copies += 1

        if previous_return_date is not None and new_return_date is None:
            # Reopening a returned loan consumes one copy.
            book = db.query(Book).filter(Book.id == loan.book_id).first()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")
            if book.available_copies <= 0:
                raise HTTPException(status_code=400, detail="No available copies")
            book.available_copies -= 1

        loan.return_date = new_return_date

    db.commit()
    db.refresh(loan)
    return loan


@router.put("/{loan_id}/return", response_model=schemas.LoanRead)
def return_loan(loan_id: int, payload: schemas.LoanReturn, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.return_date is not None:
        raise HTTPException(status_code=400, detail="Loan already returned")

    loan.return_date = payload.return_date
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book:
        book.available_copies += 1

    db.commit()
    db.refresh(loan)
    return loan


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.return_date is None:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            book.available_copies += 1

    db.delete(loan)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
