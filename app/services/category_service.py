from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Category, Expense


class CategoryNotFoundError(Exception):
    pass


class DuplicateCategoryError(Exception):
    pass


class CategoryHasExpensesError(Exception):
    pass


def get_all_categories(db: Session) -> list[Category]:
    statement = select(Category).order_by(Category.id)

    return list(db.scalars(statement).all())


def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category:
    category = db.get(Category, category_id)

    if category is None:
        raise CategoryNotFoundError

    return category


def create_category(
    db: Session,
    name: str,
) -> Category:
    existing_category = db.scalar(
        select(Category).where(
            func.lower(Category.name) == name.lower()
        )
    )

    if existing_category is not None:
        raise DuplicateCategoryError

    category = Category(name=name)

    db.add(category)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateCategoryError

    db.refresh(category)

    return category


def update_category(
    db: Session,
    category_id: int,
    name: str,
) -> Category:
    category = get_category_by_id(
        db=db,
        category_id=category_id,
    )

    duplicate_category = db.scalar(
        select(Category).where(
            func.lower(Category.name) == name.lower(),
            Category.id != category_id,
        )
    )

    if duplicate_category is not None:
        raise DuplicateCategoryError

    category.name = name

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateCategoryError

    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int,
) -> None:
    category = get_category_by_id(
        db=db,
        category_id=category_id,
    )

    expense_exists = db.scalar(
        select(Expense.id)
        .where(Expense.category_id == category_id)
        .limit(1)
    )

    if expense_exists is not None:
        raise CategoryHasExpensesError

    db.delete(category)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise CategoryHasExpensesError