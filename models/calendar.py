from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel



class Reminder(BaseModel):
    description: Optional[str]
    due_date: datetime
    status: str  # e.g., "pending", "completed"
    frequency: Optional[str]  # e.g., "weekly", "monthly", "annually"
    reminder_dates: Optional[List[datetime]]

class ReminderA(BaseModel):
    id: int
    description: Optional[str]
    due_date: datetime
    status: str  # e.g., "pending", "completed"
    frequency: Optional[str]  # e.g., "weekly", "monthly", "annually"
    reminder_dates: Optional[List[datetime]]


class ReminderUpdate(BaseModel):
    description: Optional[str]
    due_date: datetime
    status: str  # e.g., "pending", "completed"
    frequency: Optional[str]  # e.g., "weekly", "monthly", "annually"
    reminder_dates: Optional[List[datetime]]


class CalendarEvent(BaseModel):
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    event_type: str  # e.g., "income", "expense", "reminder"



class CalendarEventA(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    event_type: str  # e.g., "income", "expense", "reminder"
