
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.trackpay
users_collection = db.users
users_collection.create_index('email', unique=True)
auth_collection = db.auth
auth_collection.create_index('email', unique=True)

expense_collection = db.expenses
income_collection = db.incomes
reminder_collection = db.reminders
calendar_event_collection = db.calendar_events
custom_id_collection = db.custom_ids
token_collection = db.tokens


async def check_db_connection():
    try:
        await client.admin.command('ping')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error {e}")
