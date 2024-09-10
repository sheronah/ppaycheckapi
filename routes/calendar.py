from fastapi import APIRouter, HTTPException
from core.calendar import (
    add_reminder, get_reminders, update_reminder,
    add_calendar_event, get_calendar_events, update_calendar_event, get_single_calendar_events
)
from models.calendar import Reminder, CalendarEvent, ReminderUpdate, ReminderA, CalendarEventA

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.post("/reminders/create")
async def create_reminder(reminder: Reminder):
    reminder_id = await add_reminder(reminder)
    return {"id": reminder_id}

@router.get("/reminders/read/{reminder_id}", response_model=ReminderA)
async def read_reminders(reminder_id: int):
    reminders = await get_reminders(reminder_id)
    return reminders

@router.put("/reminders/update/{reminder_id}", response_model=ReminderA)
async def modify_reminder(reminder_id: int, reminder: ReminderUpdate):
    updated_reminder = await update_reminder(reminder_id, reminder)
    if updated_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return updated_reminder


@router.post("/calendar-events/create")
async def create_calendar_event(event: CalendarEvent):
    event_id = await add_calendar_event(event)
    return {"id": event_id}


@router.get("/calendar-events/read")
async def read_calendar_events():
    events = await get_calendar_events()
    return events


@router.get("/calendar-events/read/{event_id}", response_model=CalendarEventA)
async def read_calendar_events(event_id: int):
    events = await get_single_calendar_events(event_id)
    return events


@router.put("/calendar-events/update/{event_id}")
async def modify_calendar_event(event_id: int, event: CalendarEvent):
    updated_event = await update_calendar_event(event_id, event)
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event
