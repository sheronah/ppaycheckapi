from typing import Any
from pymongo.collection import Collection
from middleware.appDatabase import custom_id_collection
from pydantic import BaseModel


async def normal_id(collection: Collection, collection_name: str, new_record: BaseModel, **kwargs: Any):
    # Get user_id from kwargs if available
    user_id = kwargs.get('user_id', None)

    # Convert new_record (Pydantic model) to dictionary, excluding unset fields
    new_record_dict = new_record.model_dump(exclude_unset=True)

    # Generate new custom ID for the collection
    new_id = await create_ids(collection_name)

    # Update the new record dictionary with the generated ID
    if new_id is not None:
        # If user_id is provided, include it in the new record
        if user_id:
            new_record_dict = {**{"_id": new_id, "user_id": int(user_id)}, **new_record_dict}
        else:
            new_record_dict = {"_id": new_id, **new_record_dict}

        # Insert the new record into the collection
        result = await collection.insert_one(new_record_dict)

        # Check if insertion was successful
        if result.inserted_id is not None:
            return {"id": str(result.inserted_id), "status": True}

    # If the process fails, return a failure status
    return {"status": False}


async def create_ids(collection_name: str) -> int:
    try:
        # Increment the 'customs' field in the custom_id_collection for the specified collection
        result = await custom_id_collection.find_one_and_update(
            {'_id': collection_name},
            {'$inc': {'customs': 1}},
            return_document=True,
            upsert=True
        )

        # Return the updated custom ID
        return result['customs']

    except Exception as e:
        # Handle any errors that occur during ID generation
        print(f"Error generating custom ID: {e}")
        return None
