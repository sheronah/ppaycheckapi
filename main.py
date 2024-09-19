from fastapi import FastAPI, Depends

from middleware.appDatabase import check_db_connection
from middleware.tokensHashes import TokenWorks
from routes import accounts
from routes import expenses
from routes import income
from routes import calendar
app = FastAPI(dependencies=[Depends(check_db_connection), Depends(TokenWorks.invalidate_expired_tokens)])

app.include_router(accounts.router)
app.include_router(expenses.router)
app.include_router(income.router)


app.include_router(calendar.router)