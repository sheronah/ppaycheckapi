from fastapi import APIRouter, HTTPException, Depends

from modules.income_L import add_income, get_all_income, update_income, get_income
from middleware.tokensHashes import TokenWorks
from models.income_M import Income

router = APIRouter(prefix="/income", tags=["income"])


@router.post("/create_income", response_description="Add new income")
async def create_income(income: Income, user_id: int = Depends(TokenWorks.verify_token)):
    income_results = await add_income(income, user_id)
    return income_results


@router.get("/get_income", response_description="List all income")
async def read_all_income(user_id: int = Depends(TokenWorks.verify_token)):
    income = await get_all_income(user_id)
    return income


@router.put("/update_income/{income_id}", response_description="Update an income")
async def update_income_data(income_id: int, income: Income, user_id: int = Depends(TokenWorks.verify_token)):
    updated_income = await update_income(user_id, income_id, income)
    if updated_income:
        return updated_income
    raise HTTPException(status_code=404, detail=f"Income {income_id} not found")


@router.post("/get_single_income/{income_id}", response_description="Get a single income")
async def read_single_income(income_id: int, user_id: int = Depends(TokenWorks.verify_token)):
    single_income = await get_income(user_id, income_id)
    if single_income:
        return single_income
    raise HTTPException(status_code=404, detail=f"Income {income_id} not found")