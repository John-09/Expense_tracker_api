from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Category, Expense


CATEGORY_NAMES = [
    "Food",
    "Transport",
    "Rent",
    "Fun",
    "Utilities",
]


EXPENSES = [
    (
        "Food",
        "450.00",
        "Groceries",
        date(2026, 3, 2),
    ),
    (
        "Transport",
        "120.00",
        "Metro recharge",
        date(2026, 3, 4),
    ),
    (
        "Rent",
        "15000.00",
        "March rent",
        date(2026, 3, 5),
    ),
    (
        "Fun",
        "650.00",
        "Movie and snacks",
        date(2026, 3, 8),
    ),
    (
        "Food",
        "280.00",
        "Restaurant",
        date(2026, 3, 15),
    ),
    (
        "Utilities",
        "1100.00",
        "Electricity",
        date(2026, 3, 20),
    ),
    (
        "Food",
        "500.00",
        "Groceries",
        date(2026, 4, 2),
    ),
    (
        "Transport",
        "200.00",
        "Cab",
        date(2026, 4, 4),
    ),
    (
        "Rent",
        "15000.00",
        "April rent",
        date(2026, 4, 5),
    ),
    (
        "Fun",
        "900.00",
        "Day trip",
        date(2026, 4, 10),
    ),
    (
        "Food",
        "320.00",
        "Restaurant",
        date(2026, 4, 18),
    ),
    (
        "Utilities",
        "850.00",
        "Internet",
        date(2026, 4, 22),
    ),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        existing_category_id = db.scalar(
            select(Category.id).limit(1)
        )

        if existing_category_id is not None:
            print("Database already contains data. Seed skipped.")
            return

        categories = {
            name: Category(name=name)
            for name in CATEGORY_NAMES
        }

        db.add_all(categories.values())

        db.flush()

        expenses = [
            Expense(
                category_id=categories[category_name].id,
                amount=Decimal(amount),
                description=description,
                spent_on=spent_on,
            )
            for category_name, amount, description, spent_on in EXPENSES
        ]

        db.add_all(expenses)

        db.commit()

        print(
            "Seed complete: "
            "5 categories and 12 expenses inserted."
        )


if __name__ == "__main__":
    seed()