from fastapi import  Depends, HTTPException, status
from middleware import auth
from models import schemas
from fastapi.security import OAuth2PasswordRequestForm
from middleware.database import users_collection
import bcrypt

def verify_password(plain_password, hashed_password):
    plain_password = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed_password)


def get_password_hash(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt(4, b'2b')
    hashed_password = bcrypt.hashpw(password, salt).decode('utf-8')

    return hashed_password
#signup

async def new_user(user: schemas.UserCreate):
    user_in_db = await users_collection.find_one({"email": user.email})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    await users_collection.insert_one(user_dict)

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

#login
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, )

    access_token = auth.create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


#find user
async def user_me(current_user: schemas.UserCreate = Depends(auth.get_current_user)):
    user = await users_collection.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

