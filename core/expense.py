from datetime import datetime, timedelta
from bson import ObjectId

from middleware.database import expense_collection
from models.expense import Expense, ExpenseUpdate


async def add_expense(expense: Expense):
    expense = expense.dict()
    print(expense)
    result = await expense_collection.insert_one(expense)
    return str(result.inserted_id)


async def get_pending_expenses():
    expenses = await expense_collection.find({"status": "pending"}).to_list(1000)
    return expenses


async def get_previous_month_payments():
    today = datetime.today()
    first_day_of_current_month = datetime(today.year, today.month, 1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, 1)

    expenses = await expense_collection.find(
        {"due_date": {"$gte": first_day_of_previous_month, "$lt": first_day_of_current_month},
            "status": "paid"}).to_list(1000)

    return expenses


async def update_expense(id: str, expense: ExpenseUpdate):
    await expense_collection.update_one({"_id": ObjectId(id)}, {"$set": expense.dict(exclude_unset=True)})
    return await expense_collection.find_one({"_id": ObjectId(id)})


async def get_expenses_recurring():
    expenses = await expense_collection.find({"recurring": False}).to_list(1000)
    return expenses
