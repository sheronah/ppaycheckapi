from datetime import datetime, timedelta

from fastapi import HTTPException

from middleware.appDatabase import expense_collection
from middleware.extras import normal_id
from models.expense_M import Expense

# Todo: note changes
projection_expense = {"_id": 0, "expense_id": "$_id", "user_id": 1, "amount": 1, "description": 1, "due_date": 1,
    "status": 1, "frequency": 1, "recurring": 1}


async def add_expense(user_id: int, expense: Expense):
    # Todo: note changes
    results = await normal_id(expense_collection, "expenses", expense, user_id=user_id)
    if results['status']:
        exp = await expense_collection.find_one({"user_id": user_id, "_id": results["id"]}, projection_expense)
        if exp:
            return Expense(**exp)

    return HTTPException(status_code=404, detail="Error: Failed to add record", headers={"WWW-Authenticate": "Bearer"})


async def get_pending_expenses(user_id: int):
    expenses = await expense_collection.find({"user_id": user_id, "status": "pending"}, projection_expense).to_list(
        1000)
    return expenses


async def get_previous_month_payments(user_id: int):
    today = datetime.today()
    first_day_of_current_month = datetime(today.year, today.month, 1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, 1)

    # Todo: note changes
    expenses = await expense_collection.find(
        {"user_id": user_id, "due_date": {"$gte": first_day_of_previous_month, "$lt": first_day_of_current_month},
         "status": "paid"}, projection_expense).to_list(1000)

    return expenses


async def update_expense(user_id: int, expense_id: int, expense: Expense):
    rs = await expense_collection.update_one({"user_id": user_id, "_id": expense_id}, {"$set": expense.model_dump(exclude_none=True)})
    if rs.modified_count > 0:
        return await expense_collection.find_one({"user_id": user_id, "_id": expense_id}, projection_expense)
    return HTTPException(status_code=404, detail="Error: Failed to make changes", headers={"WWW-Authenticate": "Bearer"})


async def get_expenses_recurring(user_id: int, recurring: bool):
    # Todo: note changes
    expenses = await expense_collection.find({"user_id": user_id, "recurring": recurring}, projection_expense).to_list(1000)
    return expenses
