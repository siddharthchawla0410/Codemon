from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/operations", tags=["operations"])


@router.get("", response_model=list[schemas.Operation])
def list_operations(category: str | None = None, db: Session = Depends(get_db)):
    """Get all operations, optionally filtered by category."""
    return crud.get_operations(db, category)


@router.get("/{slug}", response_model=schemas.Operation)
def get_operation(slug: str, db: Session = Depends(get_db)):
    """Get a specific operation by its slug."""
    operation = crud.get_operation_by_slug(db, slug)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operation
