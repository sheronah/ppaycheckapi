from fastapi import FastAPI
from routes import user_auth
from routes import expenses
from routes import income
app = FastAPI()

app.include_router(user_auth.router)
app.include_router(expenses.router)
app.include_router(income.router)


