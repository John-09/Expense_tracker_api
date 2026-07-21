from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.summary import MonthlySummaryResponse
from app.services.summary_service import (
    InvalidSummaryMonthError,
    get_monthly_summary,
)


router = APIRouter(
    prefix="/summary",
    tags=["Summary"],
)


@router.get(
    "",
    response_model=MonthlySummaryResponse,
    status_code=status.HTTP_200_OK,
)
def monthly_summary(
    month: str | None = Query(
        default=None,
        description=(
            "Month in YYYY-MM format, "
            "for example 2026-03"
        ),
    ),
    db: Session = Depends(get_db),
):
    try:
        return get_monthly_summary(
            db=db,
            month=month,
        )
    except InvalidSummaryMonthError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )