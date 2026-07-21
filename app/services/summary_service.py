from calendar import monthrange
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Category, Expense
from app.schemas.summary import (
    CategorySummaryResponse,
    MonthlySummaryResponse,
)


class InvalidSummaryMonthError(Exception):
    pass


def parse_month(month: str | None) -> tuple[int, int]:
    if month is None:
        raise InvalidSummaryMonthError(
            "month query parameter is required. "
            "Use the YYYY-MM format, for example 2026-03."
        )

    try:
        year_text, month_text = month.split("-")

        if len(year_text) != 4 or len(month_text) != 2:
            raise ValueError

        year = int(year_text)
        month_number = int(month_text)

        if month_number < 1 or month_number > 12:
            raise ValueError

        return year, month_number

    except (ValueError, TypeError):
        raise InvalidSummaryMonthError(
            "Invalid month format. "
            "Use YYYY-MM, for example 2026-03."
        )


def get_month_date_range(
    year: int,
    month_number: int,
) -> tuple[date, date]:
    last_day = monthrange(
        year,
        month_number,
    )[1]

    first_date = date(
        year,
        month_number,
        1,
    )

    last_date = date(
        year,
        month_number,
        last_day,
    )

    return first_date, last_date


def get_monthly_summary(
    db: Session,
    month: str | None,
) -> MonthlySummaryResponse:
    year, month_number = parse_month(month)

    from_date, to_date = get_month_date_range(
        year=year,
        month_number=month_number,
    )

    statement = (
        select(
            Category.name,
            func.sum(Expense.amount).label(
                "category_total"
            ),
        )
        .join(
            Expense,
            Expense.category_id == Category.id,
        )
        .where(
            Expense.date >= from_date,
            Expense.date <= to_date,
        )
        .group_by(
            Category.id,
            Category.name,
        )
        .order_by(
            func.sum(Expense.amount).desc()
        )
    )

    rows = db.execute(statement).all()

    total_spend = sum(
        (
            row.category_total
            for row in rows
        ),
        start=Decimal("0.00"),
    )

    category_summaries = []

    for row in rows:
        category_total = row.category_total

        if total_spend == Decimal("0.00"):
            percentage = Decimal("0.00")
        else:
            percentage = (
                category_total
                / total_spend
                * Decimal("100")
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

        category_summaries.append(
            CategorySummaryResponse(
                category_name=row.name,
                total=category_total,
                percentage=percentage,
            )
        )

    return MonthlySummaryResponse(
        month=f"{year:04d}-{month_number:02d}",
        total_spend=total_spend,
        categories=category_summaries,
    )