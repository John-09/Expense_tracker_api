from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
)
from app.services.category_service import (
    CategoryHasExpensesError,
    CategoryNotFoundError,
    DuplicateCategoryError,
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    update_category,
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get(
    "",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def list_categories(
    db: Session = Depends(get_db),
):
    return get_all_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_category_by_id(
            db=db,
            category_id=category_id,
        )
    except CategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_category(
            db=db,
            name=category_data.name,
        )
    except DuplicateCategoryError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists",
        )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
def replace_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return update_category(
            db=db,
            category_id=category_id,
            name=category_data.name,
        )
    except CategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    except DuplicateCategoryError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists",
        )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    try:
        delete_category(
            db=db,
            category_id=category_id,
        )
    except CategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    except CategoryHasExpensesError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Category cannot be deleted because "
                "it still contains expenses"
            ),
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )