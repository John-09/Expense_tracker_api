from fastapi import FastAPI

from app.graphql.schema import graphql_router
from fastapi.staticfiles import StaticFiles
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


app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True,
    ),
    name="frontend",
)