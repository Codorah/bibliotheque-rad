from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str = Field(min_length=10, max_length=32)
    publication_year: int | None = None
    available_copies: int = Field(default=0, ge=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = Field(default=None, min_length=10, max_length=32)
    publication_year: int | None = None
    available_copies: int | None = Field(default=None, ge=0)


class BookRead(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MemberBase(BaseModel):
    name: str
    email: str
    membership_date: date | None = Field(default_factory=date.today)


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    membership_date: date | None = None


class MemberRead(MemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class LoanBase(BaseModel):
    book_id: int
    member_id: int
    loan_date: date | None = Field(default_factory=date.today)
    return_date: date | None = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    loan_date: date | None = None
    return_date: date | None = None


class LoanReturn(BaseModel):
    return_date: date | None = Field(default_factory=date.today)


class LoanRead(LoanBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
