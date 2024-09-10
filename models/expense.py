from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    amount: float
    description: str
    due_date: datetime
    status: str  # "paid" or "pending"
    frequency: Optional[str]  # e.g., "weekly", "monthly", "annually"
    recurring: bool = False  # New field to indicate if the expense is recurring


class ExpenseUpdate(BaseModel):
    amount: Optional[float]
    description: Optional[str]
    due_date: Optional[datetime]
    status: Optional[str]
    recurring: Optional[bool]
    frequency: Optional[str]  # e.g., "weekly", "monthly", "annually"

#output from the database,what a user will see
class ExpenseA(BaseModel):
    id: int
    amount: Optional[float]
    description: Optional[str]
    due_date: Optional[datetime]
    status: Optional[str]
    recurring: Optional[bool]
    frequency: Optional[str]

