from fastapi import FastAPI

from app.graphql.schema import graphql_router
from app.routes.categories import router as categories_router
from app.routes.expenses import router as expenses_router
from app.routes.summary import router as summary_router


app = FastAPI(
    title="Expense Tracker API",
)


app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(summary_router)

app.include_router(
    graphql_router,
    prefix="/graphql",
)


@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running"
    }