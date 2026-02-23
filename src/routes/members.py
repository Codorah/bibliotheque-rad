from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src import schemas
from src.database import get_db
from src.models.models import Loan, Member

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=schemas.MemberRead, status_code=status.HTTP_201_CREATED)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    existing = db.query(Member).filter(Member.email == member.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_member = Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/", response_model=list[schemas.MemberRead])
def list_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Member).offset(skip).limit(limit).all()


@router.get("/{member_id}", response_model=schemas.MemberRead)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/{member_id}", response_model=schemas.MemberRead)
def update_member(member_id: int, payload: schemas.MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    updates = payload.model_dump(exclude_unset=True)
    if "email" in updates and updates["email"] != member.email:
        existing = db.query(Member).filter(Member.email == updates["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    for key, value in updates.items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    active_loan = (
        db.query(Loan)
        .filter(Loan.member_id == member_id)
        .filter(Loan.return_date.is_(None))
        .first()
    )
    if active_loan:
        raise HTTPException(status_code=400, detail="Member has active loans")

    db.delete(member)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
