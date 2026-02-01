from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models


def get_languages(db: Session) -> list[models.Language]:
    return db.query(models.Language).all()


def get_language_by_slug(db: Session, slug: str) -> models.Language | None:
    return db.query(models.Language).filter(models.Language.slug == slug).first()


def get_operations(db: Session, category: str | None = None) -> list[models.Operation]:
    query = db.query(models.Operation)
    if category:
        query = query.filter(models.Operation.category == category)
    return query.order_by(models.Operation.category, models.Operation.name).all()


def get_operation_by_slug(db: Session, slug: str) -> models.Operation | None:
    return db.query(models.Operation).filter(models.Operation.slug == slug).first()


def get_categories(db: Session) -> list[dict]:
    results = (
        db.query(
            models.Operation.category,
            func.count(models.Operation.id).label("count")
        )
        .group_by(models.Operation.category)
        .all()
    )
    return [
        {"name": cat.replace("_", " ").title(), "slug": cat, "operation_count": count}
        for cat, count in results
    ]


def get_snippets(
    db: Session,
    language_slugs: list[str],
    operation_slug: str | None = None
) -> list[models.Snippet]:
    query = (
        db.query(models.Snippet)
        .join(models.Language)
        .join(models.Operation)
        .filter(models.Language.slug.in_(language_slugs))
    )
    if operation_slug:
        query = query.filter(models.Operation.slug == operation_slug)
    return query.all()


def get_snippets_for_comparison(
    db: Session,
    language_slugs: list[str],
    operation_slug: str
) -> dict:
    operation = get_operation_by_slug(db, operation_slug)
    if not operation:
        return None

    snippets = {}
    for lang_slug in language_slugs:
        snippet = (
            db.query(models.Snippet)
            .join(models.Language)
            .join(models.Operation)
            .filter(models.Language.slug == lang_slug)
            .filter(models.Operation.slug == operation_slug)
            .first()
        )
        snippets[lang_slug] = snippet

    return {"operation": operation, "snippets": snippets}
