from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Category, Expense


class ExpenseNotFoundError(Exception):
    pass


class ExpenseCategoryNotFoundError(Exception):
    pass


class InvalidExpenseDateRangeError(Exception):
    pass


def get_all_expenses(
    db: Session,
    category_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[Expense]:
    if (
        from_date is not None
        and to_date is not None
        and from_date > to_date
    ):
        raise InvalidExpenseDateRangeError

    filters = []

    if category_id is not None:
        filters.append(
            Expense.category_id == category_id
        )

    if from_date is not None:
        filters.append(
            Expense.date >= from_date
        )

    if to_date is not None:
        filters.append(
            Expense.date <= to_date
        )

    statement = (
        select(Expense)
        .options(selectinload(Expense.category))
        .where(*filters)
    )

    return list(db.scalars(statement).all())


def get_expense_by_id(
    db: Session,
    expense_id: int,
) -> Expense:
    statement = (
        select(Expense)
        .options(selectinload(Expense.category))
        .where(Expense.id == expense_id)
    )

    expense = db.scalar(statement)

    if expense is None:
        raise ExpenseNotFoundError

    return expense


def get_category_or_raise(
    db: Session,
    category_id: int,
) -> Category:
    category = db.get(Category, category_id)

    if category is None:
        raise ExpenseCategoryNotFoundError

    return category


def create_expense(
    db: Session, 
    title: str,
    amount: Decimal,
    description: str | None,
    expense_date: date,
    category_id: int,
) -> Expense:
    get_category_or_raise(
        db=db,
        category_id=category_id,
    )

    expense = Expense(
        title=title,
        amount=amount,
        description=description,
        date=expense_date,
        category_id=category_id,
    )

    db.add(expense)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(expense)

    return get_expense_by_id(
        db=db,
        expense_id=expense.id,
    )


def update_expense(
    db: Session,
    expense_id: int,
    *,
    title: str,
    amount: Decimal,
    description: str | None,
    expense_date: date,
    category_id: int,
) -> Expense:
    expense = get_expense_by_id(
        db=db,
        expense_id=expense_id,
    )

    get_category_or_raise(
        db=db,
        category_id=category_id,
    )

    expense.title = title
    expense.amount = amount
    expense.description = description
    expense.date = expense_date
    expense.category_id = category_id

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(expense)

    return get_expense_by_id(
        db=db,
        expense_id=expense.id,
    )


def delete_expense(
    db: Session,
    expense_id: int,
) -> None:
    expense = get_expense_by_id(
        db=db,
        expense_id=expense_id,
    )

    db.delete(expense)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise