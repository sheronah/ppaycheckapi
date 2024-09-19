from fastapi import HTTPException

from middleware.extras import normal_id
from middleware.appDatabase import income_collection
from models.income_M import Income

income_projection = {
    "_id": 0,
    "income_id": "$_id",
    "user_id": 1,
    "amount": 1,
    "source": 1,
    "frequency": 1,
    "date_time": 1
}


async def add_income(income: Income, user_id: int):
    if len(income.model_dump(exclude_none=True)) < 4:
        return HTTPException(status_code=404, detail="Invalid request, missing fields!",
                             headers={"WWW-Authenticate": "Bearer"})

    results = await normal_id(income_collection, "incomes", income, user_id=user_id)
    if results['status']:
        rs = await income_collection.find_one({"_id": results["id"]}, income_projection)
        if rs:
            return Income(**rs)

    return HTTPException(status_code=404, detail="Error: Failed to add record",
                         headers={"WWW-Authenticate": "Bearer"})


async def get_all_income(user_id: int):
    print(user_id)
    rs = await income_collection.find({"user_id": user_id}, income_projection).to_list(10000)
    if rs is not None:
        return rs

    return HTTPException(status_code=404, detail="Record not found",
                         headers={"WWW-Authenticate": "Bearer"})


async def update_income(user_id: int, income_id: int, income: Income):
    rs = await income_collection.update_one({"user_id": user_id, "_id": income_id},
                                            {"$set": income.model_dump(exclude_unset=True)})

    if rs.modified_count > 0:
        rs1 = await income_collection.find_one({"user_id": user_id, "_id": income_id}, income_projection)
        if rs1:
            return rs1

    return HTTPException(status_code=404, detail="Record not found, no updates made",
                         headers={"WWW-Authenticate": "Bearer"})


async def get_income(user_id: int, income_id: int):
    rs = await income_collection.find_one({"user_id": user_id, "_id": income_id}, income_projection)
    if rs is not None:
        return rs

    return HTTPException(status_code=404, detail="Record not found",
                         headers={"WWW-Authenticate": "Bearer"})
