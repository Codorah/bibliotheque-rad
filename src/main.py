from fastapi import FastAPI

from src.database import Base, engine
from src.routes.books import router as books_router
from src.routes.loans import router as loans_router
from src.routes.members import router as members_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion Bibliotheque Municipale")

app.include_router(books_router)
app.include_router(members_router)
app.include_router(loans_router)


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de la Bibliotheque"}


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
