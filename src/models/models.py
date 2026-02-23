from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    isbn: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    publication_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    available_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="book")


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    membership_date: Mapped[date | None] = mapped_column(Date, nullable=True, default=date.today)

    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="member")


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False, index=True)
    loan_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    return_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    book: Mapped["Book"] = relationship("Book", back_populates="loans")
    member: Mapped["Member"] = relationship("Member", back_populates="loans")
