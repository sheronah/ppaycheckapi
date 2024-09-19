from datetime import timedelta, datetime

from fastapi import HTTPException, status

from middleware.extras import normal_id
from middleware.appDatabase import users_collection, auth_collection
from middleware.tokensHashes import PasswordWorks, TokenWorks
from models.users_M import User, Auth, UserX


async def sign_up(user: UserX):
    user_copy = user.model_dump()
    user_in_db = await users_collection.find_one({"email": user.email})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = PasswordWorks.get_password_hash(user.password)
    user_copy.pop("password")
    user_copy = {**user_copy, **{"is_active": True, "date_joined": datetime.utcnow()}}

    rs = await normal_id(users_collection, "users", User(**user_copy))
    await auth_collection.insert_one({"email": user.email, "password": hashed_password})

    if rs['status']:
        to_tokenize = {"user_id": rs['id'], "names": user.first_name + " " + user.last_name, "email": user.email}

        access_token = TokenWorks.create_access_token(data=to_tokenize, expires_delta=timedelta(seconds=50))

        return {"details": access_token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code=400, detail="Failed to create user")


# login
async def login(login_data: Auth):
    user_auth = await auth_collection.find_one({"email": login_data.email})
    verify_pass = PasswordWorks.verify_password(login_data.password, user_auth["password"])

    if not user_auth or not verify_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})

    user = await users_collection.find_one({"email": login_data.email},
        {"_id": 0, "user_id": "$_id", "names": {"$concat": ["$first_name", " ", "$last_name"]}, "email": 1})

    to_tokenize = {"user_id": user['user_id'], "names": user['names'], "email": user["email"]}

    access_token = TokenWorks.create_access_token(data=to_tokenize)
    return {"details": access_token, "token_type": "bearer"}


# find user
async def user_me(user_id: int):
    u = await users_collection.find_one({"_id": user_id})
    if u is None:
        raise HTTPException(status_code=404, detail="User not found")
    return u
