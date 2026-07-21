from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

import strawberry

from app.models import Category, Expense


if TYPE_CHECKING:
    from app.graphql.types import CategoryType


@strawberry.type
class CategoryExpenseType:
    id: int
    title: str
    amount: Decimal
    description: str | None
    date: date
    category_id: int

    @classmethod
    def from_model(
        cls,
        expense: Expense,
    ) -> "CategoryExpenseType":
        return cls(
            id=expense.id,
            title=expense.title,
            amount=expense.amount,
            description=expense.description,
            date=expense.date,
            category_id=expense.category_id,
        )


@strawberry.type
class ExpenseType:
    id: int
    title: str
    amount: Decimal
    description: str | None
    date: date
    category_id: int

    _model: strawberry.Private[Expense]

    @strawberry.field
    def category(self) -> "CategoryType":
        return CategoryType.from_model(
            self._model.category
        )

    @classmethod
    def from_model(
        cls,
        expense: Expense,
    ) -> "ExpenseType":
        return cls(
            id=expense.id,
            title=expense.title,
            amount=expense.amount,
            description=expense.description,
            date=expense.date,
            category_id=expense.category_id,
            _model=expense,
        )


@strawberry.type
class CategoryType:
    id: int
    name: str

    _model: strawberry.Private[Category]

    @strawberry.field
    def expenses(self) -> list[CategoryExpenseType]:
        return [
            CategoryExpenseType.from_model(expense)
            for expense in self._model.expenses
        ]

    @classmethod
    def from_model(
        cls,
        category: Category,
    ) -> "CategoryType":
        return cls(
            id=category.id,
            name=category.name,
            _model=category,
        )