from decimal import Decimal

from pydantic import BaseModel


class CategorySummaryResponse(BaseModel):
    category_name: str
    total: Decimal
    percentage: Decimal


class MonthlySummaryResponse(BaseModel):
    month: str
    total_spend: Decimal
    categories: list[CategorySummaryResponse]