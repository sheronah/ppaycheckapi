from fastapi import APIRouter, HTTPException, Depends
from modules.calendar_L import (
    add_reminder, get_reminders, update_reminder,
    add_calendar_event, get_calendar_events, update_calendar_event, get_single_calendar_events
)
from middleware.tokensHashes import TokenWorks
from models.calendar_M import Reminder, CalendarEvent

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.post("/reminders/create")
async def create_reminder(reminder: Reminder, user_id: int = Depends(TokenWorks.verify_token)):
    reminder = await add_reminder(user_id, reminder)
    return reminder


@router.get("/reminders/read/{reminder_id}", response_model=Reminder)
async def read_reminders(reminder_id: int, user_id: int = Depends(TokenWorks.verify_token)):
    reminders = await get_reminders(user_id, reminder_id)
    return reminders


@router.put("/reminders/update/{reminder_id}", response_model=Reminder)
async def modify_reminder(reminder_id: int, reminder: Reminder, user_id: int = Depends(TokenWorks.verify_token)):
    updated_reminder = await update_reminder(user_id, reminder_id, reminder)
    if updated_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return updated_reminder


@router.post("/calendar-events/create")
async def create_calendar_event(event: CalendarEvent, user_id: int = Depends(TokenWorks.verify_token)):
    event_id = await add_calendar_event(user_id, event)
    return event_id


@router.get("/calendar-events/read")
async def read_calendar_events(user_id: int = Depends(TokenWorks.verify_token)):
    events = await get_calendar_events(user_id)
    return events


@router.get("/calendar-events/read/{event_id}", response_model=CalendarEvent)
async def read_calendar_events(event_id: int, user_id: int = Depends(TokenWorks.verify_token)):
    events = await get_single_calendar_events(user_id, event_id)
    return events


@router.put("/calendar-events/update/{event_id}")
async def modify_calendar_event(event_id: int, event: CalendarEvent, user_id: int = Depends(TokenWorks.verify_token)):
    updated_event = await update_calendar_event(user_id, event_id, event)
    return updated_event
