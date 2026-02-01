from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/snippets", tags=["snippets"])

MAX_LANGUAGES = 3


def parse_languages(languages: str) -> list[str]:
    """Parse comma-separated language slugs and validate count."""
    lang_list = [lang.strip().lower() for lang in languages.split(",") if lang.strip()]
    if len(lang_list) > MAX_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {MAX_LANGUAGES} languages allowed"
        )
    if not lang_list:
        raise HTTPException(status_code=400, detail="At least one language required")
    return lang_list


@router.get("", response_model=list[schemas.SnippetWithDetails])
def get_snippets(
    languages: str = Query(..., description="Comma-separated language slugs (max 3)"),
    operation: str | None = Query(None, description="Operation slug to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get code snippets for selected languages.

    - **languages**: Comma-separated list of language slugs (e.g., "python,javascript,java")
    - **operation**: Optional operation slug to filter snippets
    """
    lang_list = parse_languages(languages)
    snippets = crud.get_snippets(db, lang_list, operation)
    return snippets


@router.get("/compare", response_model=schemas.SnippetComparison)
def compare_snippets(
    languages: str = Query(..., description="Comma-separated language slugs (max 3)"),
    operation: str = Query(..., description="Operation slug to compare"),
    db: Session = Depends(get_db)
):
    """
    Compare code snippets across languages for a specific operation.

    Returns snippets side-by-side for easy comparison.
    """
    lang_list = parse_languages(languages)
    result = crud.get_snippets_for_comparison(db, lang_list, operation)
    if not result:
        raise HTTPException(status_code=404, detail="Operation not found")
    return result
