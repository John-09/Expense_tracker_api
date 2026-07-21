import os
from dotenv import load_dotenv

# This line tells Python to look for a file named '.env' and load its variables
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://expense_user:expense_password@localhost:5432/expense_tracker",
)