from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Income(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    amount: float
    source: str
    frequency: str  # e.g., "monthly", "weekly"
    date_time: datetime

class IncomeA(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    amount: float
    source: str
    frequency: str  # e.g., "monthly", "weekly"
    date_time: datetime

class IncomeUpdate(BaseModel):
    amount: Optional[float]
    source: Optional[str]
    frequency: Optional[str]
    date_time: Optional[datetime]
