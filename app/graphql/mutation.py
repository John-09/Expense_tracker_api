import strawberry
from strawberry.types import Info

from app.graphql.context import GraphQLContext
from app.graphql.inputs import AddExpenseInput
from app.graphql.types import ExpenseType
from app.services.expense_service import (
    ExpenseCategoryNotFoundError,
    ExpenseNotFoundError,
    create_expense,
    delete_expense,
)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_expense(
        info: Info[GraphQLContext, None],
        input: AddExpenseInput,
    ) -> ExpenseType:
        db = info.context["db"]

        if not input.title.strip():
            raise ValueError(
                "Expense title cannot be empty"
            )

        if input.amount <= 0:
            raise ValueError(
                "Expense amount must be greater than zero"
            )

        try:
            expense = create_expense(
                db=db,
                title=input.title.strip(),
                amount=input.amount,
                description=(
                    input.description.strip()
                    if input.description
                    else None
                ),
                expense_date=input.date,
                category_id=input.category_id,
            )
        except ExpenseCategoryNotFoundError:
            raise ValueError(
                f"Category with id {input.category_id} "
                "was not found"
            )

        return ExpenseType.from_model(expense)

    @strawberry.mutation
    def delete_expense(
        info: Info[GraphQLContext, None],
        id: int,
    ) -> bool:
        db = info.context["db"]

        try:
            delete_expense(
                db=db,
                expense_id=id,
            )
        except ExpenseNotFoundError:
            raise ValueError(
                f"Expense with id {id} was not found"
            )

        return True