# route/income.py
from typing import List

from fastapi import APIRouter, HTTPException

from core.income import add_income, get_all_income, update_income, get_income
from models.income import Income, IncomeUpdate, IncomeA

router = APIRouter(prefix="/income", tags=["income"])


@router.post("/create_income", response_description="Add new income")
async def create_income(income: Income):
    income_id = await add_income(income)
    return {"id": income_id}


@router.get("/get_income", response_description="List all income")
async def read_all_income():
    income = await get_all_income()
    return income


@router.put("/update_income/{id}", response_description="Update an income")
async def update_income_data(id: str, income: IncomeUpdate):
    updated_income = await update_income(id, income)
    if updated_income:
        return updated_income
    raise HTTPException(status_code=404, detail=f"Income {id} not found")


@router.post("/get_single_income/{id}", response_description="Get a single income")
async def read_single_income(id: str):
    rs = await get_income(id)
    if rs:
        return rs
    else:
        raise HTTPException(status_code=404, detail=f"Income {id} not found")
