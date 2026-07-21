from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.services.expense_service import (
    ExpenseCategoryNotFoundError,
    ExpenseNotFoundError,
    create_expense,
    delete_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.get(
    "",
    response_model=list[ExpenseResponse],
    status_code=status.HTTP_200_OK,
)
def list_expenses(
    db: Session = Depends(get_db),
):
    return get_all_expenses(db)


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    status_code=status.HTTP_200_OK,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_expense_by_id(
            db=db,
            expense_id=expense_id,
        )
    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_expense(
            db=db,
            title=expense_data.title,
            amount=expense_data.amount,
            expense_date=expense_data.date,
            description=expense_data.description,
            category_id=expense_data.category_id,
        )
    except ExpenseCategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
    status_code=status.HTTP_200_OK,
)
def replace_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
):
    try:
        return update_expense(
            db=db,
            expense_id=expense_id,
            title=expense_data.title,
            amount=expense_data.amount,
            expense_date=expense_data.date,
            description=expense_data.description,
            category_id=expense_data.category_id,
        )
    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )
    except ExpenseCategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_expense(
            db=db,
            expense_id=expense_id,
        )
    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )