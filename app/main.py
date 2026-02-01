from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, crud, schemas
from .database import engine, get_db
from .routers import languages, operations, snippets
from fastapi import Depends
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Codemon API",
    description="API for code snippets learning - compare boilerplate code across programming languages",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(languages.router)
app.include_router(operations.router)
app.include_router(snippets.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Codemon API",
        "docs": "/docs",
        "endpoints": {
            "languages": "/api/languages",
            "operations": "/api/operations",
            "snippets": "/api/snippets",
            "categories": "/api/categories"
        }
    }


@app.get("/api/categories", response_model=list[schemas.Category], tags=["categories"])
def list_categories(db: Session = Depends(get_db)):
    """Get all operation categories with their counts."""
    return crud.get_categories(db)
