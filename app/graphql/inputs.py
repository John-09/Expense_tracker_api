from datetime import date
from decimal import Decimal

import strawberry


@strawberry.input
class AddExpenseInput:
    title: str
    amount: Decimal
    description: str | None
    date: date
    category_id: int