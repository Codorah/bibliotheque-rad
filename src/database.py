import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

def _default_database_url() -> str:
    if os.getenv("VERCEL"):
        return "sqlite:////tmp/library.db"
    return "sqlite:///./library.db"


def _normalize_database_url(raw_url: str | None) -> str:
    if not raw_url:
        return _default_database_url()

    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql+psycopg2://", 1)

    if raw_url.startswith("postgresql://") and "+psycopg2" not in raw_url:
        return raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    return raw_url


DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL"))

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
