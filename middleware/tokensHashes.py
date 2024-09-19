from datetime import datetime, timedelta
from typing import Union

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, PyJWTError as JWTError

from middleware.appDatabase import token_collection


class TokenWorks:
    # Secret key and algorithm to encode/decode JWT
    _SECRET_KEY = ("When Jesus Comes, we Shall rise with him, we shall rise and "
                   "live for eternity, note(Ashabahebwa's words-secret)")
    _ALGORITHM = "HS256"
    _ACCESS_TOKEN_EXPIRE_MINUTES = 30

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=TokenWorks._ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, TokenWorks._SECRET_KEY, algorithm=TokenWorks._ALGORITHM)

        to_save = {"user_id": data['user_id'], "username": data['names'], "access_token": encoded_jwt,
                   "token_type": "bearer", "expires_in": expire, "date_created": datetime.utcnow(), "is_active": True}

        results = token_collection.insert_one(to_save)

        if results:
            return to_save
        else:
            return None

    @staticmethod
    async def verify_token(token: str = Depends(oauth2_scheme), credentials_exception=None):
        if credentials_exception is None:
            credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail="Could not validate credentials")
        try:
            payload = jwt.decode(token, TokenWorks._SECRET_KEY, algorithms=[TokenWorks._ALGORITHM])
            user_id: str = payload.get("user_id")
            return user_id

        except ExpiredSignatureError:
            await token_collection.update_one({"access_token": token}, {"$set": {"is_active": False}})
            raise credentials_exception
        except JWTError as e:
            raise HTTPException(status_code=404, detail="Something went wrong", headers={"WWW-Authenticate": "Bearer"})

    @staticmethod
    async def invalidate_expired_tokens():
        results = await token_collection.update_many(
            {"is_active": True, "expires_in": {"$lt": datetime.utcnow()}}, {"$set": {"is_active": False}},
            upsert=False)




class PasswordWorks:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        plain_password = plain_password.encode('utf-8')
        hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        password = password.encode('utf-8')
        salt = bcrypt.gensalt(4, b'2b')
        hashed_password = bcrypt.hashpw(password, salt).decode('utf-8')

        return hashed_password
