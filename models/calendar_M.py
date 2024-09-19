from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from pydantic.fields import Field


class Reminder(BaseModel):
    reminder_id: Optional[int] = Field(None, alias='reminder_id')
    user_id: Optional[int] = Field(None, alias="user_id")
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None  # e.g., "pending", "completed"
    frequency: Optional[str] = None  # e.g., "weekly", "monthly", "annually"
    reminder_dates: Optional[List[datetime]] = None


class CalendarEvent(BaseModel):
    event_id: Optional[int] = Field(None, alias='event_id')
    user_id: Optional[int] = Field(None, alias="user_id")
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: datetime = None
    end_date: datetime = None
    event_type: str = None # e.g., "income", "expense", "reminder"



