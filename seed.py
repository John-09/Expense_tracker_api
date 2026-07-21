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
        "Grocery shopping",
    ),
    (
        "Transport",
        "120.00",
        "Metro recharge",
        date(2026, 3, 4),
        "Metro card recharge",
    ),
    (
        "Rent",
        "15000.00",
        "March rent",
        date(2026, 3, 5),
        "Monthly house rent",
    ),
    (
        "Fun",
        "650.00",
        "Movie and snacks",
        date(2026, 3, 8),
        "Movie night",
    ),
    (
        "Food",
        "280.00",
        "Restaurant",
        date(2026, 3, 15),
        None,
    ),
    (
        "Utilities",
        "1100.00",
        "Electricity",
        date(2026, 3, 20),
        "Electricity bill",
    ),
    (
        "Food",
        "500.00",
        "Groceries",
        date(2026, 4, 2),
        "Grocery shopping",
    ),
    (
        "Transport",
        "200.00",
        "Cab",
        date(2026, 4, 4),
        "Taxi ride",
    ),
    (
        "Rent",
        "15000.00",
        "April rent",
        date(2026, 4, 5),
        "Monthly house rent",
    ),
    (
        "Fun",
        "900.00",
        "Day trip",
        date(2026, 4, 10),
        "Day trip to the countryside",
    ),
    (
        "Food",
        "320.00",
        "Restaurant",
        date(2026, 4, 18),
        "Dinner with friends",
    ),
    (
        "Utilities",
        "850.00",
        "Internet",
        date(2026, 4, 22),
        "Fiber internet bill",
    ),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        existing_category = db.scalar(
            select(Category.id).limit(1)
        )

        if existing_category is not None:
            print("Database already contains data. Seed skipped.")
            return

        categories = {
            name: Category(name=name)
            for name in CATEGORY_NAMES
        }

        db.add_all(categories.values())

        # Inserts the categories first so they receive IDs.
        # Those IDs are needed while creating expenses.
        db.flush()

        expenses = [
            Expense(
                title=title,
                amount=Decimal(amount),
                description=description,
                date=expense_date,
                category_id=categories[category_name].id,
            )
            for (
                category_name,
                amount,
                title,
                expense_date,
                description,
            ) in EXPENSES
        ]

        db.add_all(expenses)

        db.commit()

        print(
            "Seed complete: "
            "5 categories and 12 expenses inserted."
        )


if __name__ == "__main__":
    seed()