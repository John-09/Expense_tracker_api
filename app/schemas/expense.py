from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.category import CategoryResponse


class ExpenseCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=150,
        examples=["Lunch"],
    )

    amount: Decimal = Field(
        gt=0,
        decimal_places=2,
        examples=[250.50],
    )

    date: date

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    category_id: int = Field(gt=0)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned_title = value.strip()

        if not cleaned_title:
            raise ValueError("Expense title cannot be empty")

        return cleaned_title

    @field_validator("description")
    @classmethod
    def validate_description(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned_description = value.strip()

        return cleaned_description or None


class ExpenseUpdate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=150,
    )

    amount: Decimal = Field(
        gt=0,
        decimal_places=2,
    )

    date: date

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    category_id: int = Field(gt=0)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned_title = value.strip()

        if not cleaned_title:
            raise ValueError("Expense title cannot be empty")

        return cleaned_title

    @field_validator("description")
    @classmethod
    def validate_description(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        cleaned_description = value.strip()

        return cleaned_description or None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    amount: Decimal
    date: date
    description: str | None
    category_id: int
    category: CategoryResponse