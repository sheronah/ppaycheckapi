# core/income.py

from bson import ObjectId

from middleware.database import income_collection
from models.income import Income, IncomeUpdate, IncomeA


async def add_income(income: Income):
    income = income.dict()
    result = await income_collection.insert_one(income)
    return str(result.inserted_id)


async def get_all_income():
    income = await income_collection.find().to_list(10000)
    final_in = []
    for i in income:
        i = dict(i)
        final_in.append(IncomeA(
            id=ObjectId(i['_id']).__str__(),
            amount=i["amount"],
            source=i['source'],
            frequency=i['frequency'],
            date_time=i['date_time'],
        ))

    return final_in


async def update_income(id: str, income: IncomeUpdate):
    await income_collection.update_one({"_id": ObjectId(id)}, {"$set": income.dict(exclude_unset=True)})
    rs = await income_collection.find_one({"_id": ObjectId(id)})

    return IncomeA(
            id=ObjectId(rs['_id']).__str__(),
            amount=rs['amount'],
            source=rs['source'],
            frequency=rs['frequency'],
            date_time=rs['date_time'],
        )


async def get_income(id: str):
    rs = await income_collection.find_one({"_id": ObjectId(id)})
    if rs is None:
        return None
    else:
        return IncomeA(
            id=ObjectId(rs['_id']).__str__(),
            amount=rs['amount'],
            source=rs['source'],
            frequency=rs['frequency'],
            date_time=rs['date_time'],
        )