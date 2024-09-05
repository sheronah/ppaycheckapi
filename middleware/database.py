from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.trackpays
users_collection = db.users
expense_collection = db.expenses
income_collection = db.incomes

