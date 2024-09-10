

from middleware.database import income_collection
from models.income import Income, IncomeUpdate, IncomeA
from .datefunc import normal_id

projection_income = {

    "_id": 0,
    "id": "$_id",
    "amount": 1,
    "source": 1,
    "frequency": 1,
    "date_time": 1
}


async def add_income(income: Income):
    result = await normal_id(income_collection,income)
    if result['status']:
        return result['id']

    return False


async def get_all_income():
    income = await income_collection.find({}, projection_income).to_list(1000)
    return income

async def update_income(id: int, income: IncomeUpdate):
    result = await income_collection.update_one({"_id": id}, {"$set": income.dict(exclude_unset=True)})

    if result.modified_count:
        updated_income = await income_collection.find_one({"_id": id}, projection_income)
        if updated_income:

            return IncomeA(**updated_income)

    return None

async def get_income(id: int):
    rs = await income_collection.find_one({"_id": id}, projection_income)
    if rs is None:
        return None
    return IncomeA(**rs)

