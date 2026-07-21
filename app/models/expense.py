from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    from app.models.category import Category


class Expense(Base):
    __tablename__ = "expenses"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_expenses_amount_positive",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    spent_on: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    category: Mapped["Category"] = relationship(
        back_populates="expenses",
    )