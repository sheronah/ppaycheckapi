from datetime import datetime, timedelta

from fastapi import HTTPException

from middleware.appDatabase import reminder_collection, calendar_event_collection
from middleware.extras import normal_id
from models.calendar_M import Reminder, CalendarEvent

projection_cal_events = {"_id": 0, "event_id": "$_id", "user_id": 1, "title": 1, "description": 1, "start_date": 1,
                         "end_date": 1, "event_type": 1}

projection_remind = {"_id": 0, "reminder_id": "$_id", "user_id": 1, "description": 1, "due_date": 1, "status": 1,
                     "frequency": 1,
                     "reminder_dates": 1}


def calculate_reminder_dates(due_date: datetime, frequency: str):
    reminder_dates = []
    if frequency == "weekly":
        reminder_dates.append(due_date - timedelta(days=2))
    elif frequency == "monthly":
        reminder_dates.append(due_date - timedelta(days=5))
    elif frequency == "annually":
        reminder_dates.append(due_date - timedelta(days=10))
    return reminder_dates


async def add_reminder(user_id: int, reminder: Reminder):
    results = await normal_id(reminder_collection, "reminders", reminder, user_id=user_id)
    if results['status']:
        rm = await reminder_collection.find_one({"_id": results['id'], "user_id": user_id})
        if rm:
            return rm

    raise HTTPException(status_code=404, detail="Error: Failed to add record",
                        headers={"WWW-Authenticate": "Bearer"})


async def get_reminders(user_id: int, reminders_id):
    reminders = await reminder_collection.find_one({"_id": reminders_id, "user_id": user_id}, projection_remind)

    if reminders:
        return reminders

    raise HTTPException(status_code=404, detail=f"No reminder found with ID: {reminders_id}")


async def update_reminder(user_id: int, reminder_id: int, reminder: Reminder):
    result = await reminder_collection.update_one({"_id": reminder_id, "user_id": user_id},
                                                  {"$set": reminder.model_dump(exclude_none=True)})
    if result.modified_count > 0:
        updated_reminder = await reminder_collection.find_one({"user_id": user_id, "_id": reminder_id},
                                                              projection_remind)
        if updated_reminder:
            return Reminder(**updated_reminder)

    raise HTTPException(status_code=404, detail="Record not found, no updates made",
                        headers={"WWW-Authenticate": "Bearer"})


async def add_calendar_event(user_id: int, event: CalendarEvent):
    # Todo: note changes, now using the normal_id function
    results = await normal_id(calendar_event_collection, "calender_events", event, user_id=user_id)
    if results['status']:
        rs = await calendar_event_collection.find_one({"user_id": user_id, "_id": results['id']}, projection_cal_events)
        if rs:
            return CalendarEvent(**rs)

    raise HTTPException(status_code=404, detail="Error: Failed to add record",
                        headers={"WWW-Authenticate": "Bearer"})


async def get_calendar_events(user_id: int):
    # Todo: note changes
    events = await calendar_event_collection.find({"user_id": user_id}, projection_cal_events).to_list(1000)
    if events:
        return events

    raise HTTPException(status_code=404, detail=f"No Events found of user ID: {user_id}")


async def get_single_calendar_events(user_id: int, event_id: int):
    # Todo: note changes
    events = await calendar_event_collection.find_one({"_id": event_id, "user_id": user_id}, projection_cal_events)
    if events:
        return events

    raise HTTPException(status_code=404, detail=f"No Event found with id: {event_id}")


async def update_calendar_event(user_id: int, cal_id: int, event: CalendarEvent):
    # Todo: note changes, removed the ObjectID object casters
    event = await calendar_event_collection.update_one({"_id": cal_id, "user_id": user_id},
                                                       {"$set": event.model_dump(exclude_none=True)})

    if event.modified_count > 0:
        updated_event = await calendar_event_collection.find_one({"_id": cal_id, "user_id": user_id},
                                                                 projection_cal_events)
        if updated_event:
            return updated_event

    raise HTTPException(status_code=404, detail=f"Error: No record  found with ID {cal_id}, no updates made",
                        headers={"WWW-Authenticate": "Bearer"})
