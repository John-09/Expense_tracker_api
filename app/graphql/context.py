from typing import TypedDict

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db


class GraphQLContext(TypedDict):
    db: Session


def get_graphql_context(
    db: Session = Depends(get_db),
) -> GraphQLContext:
    return {
        "db": db,
    }