from typing import List

from fastapi import APIRouter, HTTPException, Depends

from modules.expense_L import add_expense, get_pending_expenses, get_previous_month_payments, update_expense, \
    get_expenses_recurring
from middleware.tokensHashes import TokenWorks
from models.expense_M import Expense

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/create", response_description="Add new expense")
async def create_expense(expense: Expense, user_id: int = Depends(TokenWorks.verify_token)):
    expense_id = await add_expense(user_id, expense)
    return {"id": expense_id}


@router.get("/read/pending", response_model=List[Expense], response_description="List all pending expenses")
async def read_pending_expenses(user_id: int = Depends(TokenWorks.verify_token)):
    expenses = await get_pending_expenses(user_id)
    return expenses


@router.get("/read/previous_month", response_model=List[Expense], response_description="Summary of previous month's payments")
async def read_previous_month_payments(user_id: int = Depends(TokenWorks.verify_token)):
    expenses = await get_previous_month_payments(user_id)
    return expenses


@router.put("/update/{expense_id}", response_model=Expense, response_description="Update an expense")
async def update_expense_data(expense_id: int, expense: Expense, user_id: int = Depends(TokenWorks.verify_token)):
    updated_expense = await update_expense(user_id, expense_id, expense)
    if updated_expense:
        return updated_expense
    raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")


@router.get("/read/recurring/{recurring}", response_model=List[Expense], response_description="List all single expenses")
async def read_single_expenses(recurring: bool, user_id: int = Depends(TokenWorks.verify_token)):
    expenses = await get_expenses_recurring(user_id, recurring)
    return expenses
