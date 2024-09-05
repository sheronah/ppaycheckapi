from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Expense(BaseModel):
    amount: float
    description: str
    due_date: datetime
    status: str  # "paid" or "pending"
    recurring: bool = False  # New field to indicate if the expense is recurring


class ExpenseUpdate(BaseModel):
    amount: Optional[float]
    description: Optional[str]
    due_date: Optional[datetime]
    status: Optional[str]
    recurring: Optional[bool]
