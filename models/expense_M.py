from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class Expense(BaseModel):
    expense_id: Optional[int] = Field(None)
    user_id: Optional[int] = Field(None, alias="user_id")
    amount: Optional[float] = Field(default=None)
    description: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None)  # "paid" or "pending"
    frequency: Optional[str] = Field(default=None)  # e.g., "weekly", "monthly", "annually"
    recurring: Optional[bool] = Field(default=None)  # New field to indicate if the expense is recurring


