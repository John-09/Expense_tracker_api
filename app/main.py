from fastapi import FastAPI

import app.models
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running"
    }