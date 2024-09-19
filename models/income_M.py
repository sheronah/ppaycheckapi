from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class Income(BaseModel):
    income_id: Optional[int] = None
    user_id: Optional[int] = Field(None, alias="user_id")
    amount: Optional[float] = None
    source: Optional[str] = None
    frequency: Optional[str] = None  # e.g., "monthly", "weekly"
    date_time: Optional[datetime] = None

