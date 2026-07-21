from fastapi import FastAPI

import app.models
from app.database import Base, engine

from app.routes.categories import router as categories_router
from app.routes.expenses import router as expenses_router
from app.routes.summary import router as summary_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(summary_router)


@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running"
    }

