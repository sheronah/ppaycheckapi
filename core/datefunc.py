from typing import Any
async def normal_id(collection: Any,new_record:Any) :
    new_id = 0

    # get last document from db inorder to extract last _id
    last_item = await collection.find().sort('_id', -1).limit(1).to_list(1)
    # change new data to dictionary
    new_record = new_record.model_dump()

    if last_item:
        # generate new id based on previous ID in database
        new_id = last_item[0]["_id"] + 1

    # update our dictionary of new data with the new custom ID that we have generated
    new_record = {**{"_id": new_id}, **new_record}

    result = await collection.insert_one(new_record)

    if result.inserted_id:
        return {"id": result.inserted_id, "status": "Successful"}

