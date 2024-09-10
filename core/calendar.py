from datetime import datetime, timedelta

from fastapi import HTTPException

from middleware.database import reminder_collection, calendar_event_collection
from models.calendar import Reminder, CalendarEvent, ReminderUpdate, ReminderA
from .datefunc import normal_id


projection_cal_events = {
    "_id": 0,
    "id": "$_id",
    "title": 1,
    "description": 1,
    "start_date": 1,
    "end_date": 1,
    "event_type": 1
}

projection_remind = {
    "_id": 0,
    "id": "$_id",
    "description": 1,
    "due_date": 1,
    "status": 1,
    "frequency": 1,
    "reminder_dates": 1
}


def calculate_reminder_dates(due_date: datetime, frequency: str):
    reminder_dates = []
    if frequency == "weekly":
        reminder_dates.append(due_date - timedelta(days=2))
    elif frequency == "monthly":
        reminder_dates.append(due_date - timedelta(days=5))
    elif frequency == "annually":
        reminder_dates.append(due_date - timedelta(days=10))
    return reminder_dates


async def add_reminder(reminder: Reminder):
    results = await normal_id(reminder_collection, reminder)
    if results['status']:
        return results['id']

    return False


async def get_reminders(reminders_id):
    reminders = await reminder_collection.find_one({"_id": reminders_id}, projection_remind)

    if reminders:
        return reminders
    raise HTTPException(status_code=404, detail="No reminders found")


async def update_reminder(reminder_id: int, reminder: ReminderUpdate):
    result = await reminder_collection.update_one({"_id": reminder_id},
                                                  {"$set": reminder.model_dump(exclude_unset=True)})
    if result.modified_count:

        updated_reminder = await reminder_collection.find_one({"_id": reminder_id}, projection_remind)
        if updated_reminder:
            return ReminderA(**updated_reminder)
    return None


async def add_calendar_event(event: CalendarEvent):
    results = await normal_id(calendar_event_collection, event)
    if results['status']:
        return results['id']

    return False


async def get_calendar_events():
    events = await calendar_event_collection.find({}, projection_cal_events).to_list(1000)
    return events


async def get_single_calendar_events(event_id: int):
    events = await calendar_event_collection.find_one({"_id": event_id}, projection_cal_events)
    return events


async def update_calendar_event(id: int, event: CalendarEvent):
    await calendar_event_collection.update_one({"_id": id}, {"$set": event.dict(exclude_unset=True)})

    updated_event = await calendar_event_collection.find_one({"_id": id}, projection_cal_events)
    return updated_event
