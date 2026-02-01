from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/languages", tags=["languages"])


@router.get("", response_model=list[schemas.Language])
def list_languages(db: Session = Depends(get_db)):
    """Get all available programming languages."""
    return crud.get_languages(db)


@router.get("/{slug}", response_model=schemas.Language)
def get_language(slug: str, db: Session = Depends(get_db)):
    """Get a specific language by its slug."""
    language = crud.get_language_by_slug(db, slug)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language
