from datetime import date

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from strawberry.types import Info

from app.graphql.context import GraphQLContext
from app.graphql.types import (
    CategoryType,
    ExpenseType,
)
from app.models import Category, Expense
from app.services.expense_service import (
    InvalidExpenseDateRangeError,
    get_all_expenses,
)


@strawberry.type
class Query:
    @strawberry.field
    def expenses(
        info: Info[GraphQLContext, None],
        category_id: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[ExpenseType]:
        db = info.context["db"]

        try:
            expenses = get_all_expenses(
                db=db,
                category_id=category_id,
                from_date=from_date,
                to_date=to_date,
            )
        except InvalidExpenseDateRangeError:
            raise ValueError(
                "fromDate cannot be later than toDate"
            )

        return [
            ExpenseType.from_model(expense)
            for expense in expenses
        ]

    @strawberry.field
    def categories(
        info: Info[GraphQLContext, None],
    ) -> list[CategoryType]:
        db = info.context["db"]

        statement = (
            select(Category)
            .options(
                selectinload(Category.expenses)
            )
        )

        categories = list(
            db.scalars(statement).all()
        )

        return [
            CategoryType.from_model(category)
            for category in categories
        ]