from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    date_joined: datetime


class UserX(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class Auth(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    user_id: str
    access_token: str
    token_type: str
    expires_in: int
    date_created: datetime
    is_active: bool
