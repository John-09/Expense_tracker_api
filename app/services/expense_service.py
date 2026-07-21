from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Category, Expense


class ExpenseNotFoundError(Exception):
    pass


class ExpenseCategoryNotFoundError(Exception):
    pass


def get_all_expenses(db: Session) -> list[Expense]:
    statement = (
        select(Expense)
        .options(selectinload(Expense.category))
        .order_by(Expense.date.desc(), Expense.id.desc())
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
    *,
    title: str,
    amount,
    expense_date,
    description: str | None,
    category_id: int,
) -> Expense:
    get_category_or_raise(
        db=db,
        category_id=category_id,
    )

    expense = Expense(
        title=title,
        amount=amount,
        date=expense_date,
        description=description,
        category_id=category_id,
    )

    db.add(expense)
    db.commit()
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
    amount,
    expense_date,
    description: str | None,
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
    expense.date = expense_date
    expense.description = description
    expense.category_id = category_id

    db.commit()
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
    db.commit()