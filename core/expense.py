from datetime import datetime, timedelta

from middleware.database import expense_collection
from models.expense import Expense, ExpenseUpdate,ExpenseA
from core.datefunc import normal_id

projection_expenses = {
    "_id": 0,
    "id": "$_id",
    "amount": 1,
    "description": 1,
    "due_date": 1,
    "status": 1,
    "recurring": 1,
    "frequency": 1
}



async def add_expense(expense: Expense):
    result = await normal_id(expense_collection,expense)
    if result['status']:
     return result['id']
    return False

async def get_pending_expenses():
    expenses = await expense_collection.find({"status": "pending"}, projection=projection_expenses).to_list(1000)
    return expenses


async def get_previous_month_payments():
    today = datetime.today()
    first_day_of_current_month = datetime(today.year, today.month, 1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, 1)

    expenses = await expense_collection.find(
        {"due_date": {"$gte": first_day_of_previous_month, "$lt": first_day_of_current_month},
         "status": "paid"}
    ).to_list(1000)

    # Ensure _id is converted to id and remove the _id key
    transformed_expenses = []
    for expense in expenses:
        if '_id' in expense:
            expense['id'] = int(expense.pop('_id'))  # Convert _id to id
        transformed_expenses.append(expense)

    return transformed_expenses




async def update_expense(id: int, expense: ExpenseUpdate):
    await expense_collection.update_one({"_id": id}, {"$set": expense.dict(exclude_unset=True)})
    updated_expense = await expense_collection.find_one({"_id": id},projection_expenses)
    if updated_expense:
            return ExpenseA(**updated_expense)
    return None


async def get_expenses_recurring():
    expenses = await expense_collection.find({"recurring": False},projection_expenses).to_list(1000)
    return expenses
