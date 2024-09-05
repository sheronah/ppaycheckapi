from fastapi import APIRouter, Depends, HTTPException, status
from middleware import auth
from models import schemas
from fastapi.security import OAuth2PasswordRequestForm

from core.user import new_user,login,user_me
router = APIRouter()



@router.post("/signup", response_model=schemas.Token)
async def create_user(user: schemas.UserCreate):
    return await new_user(user)
@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data)

@router.get("/users/me", response_model=schemas.UserCreate)
async def read_users_me(current_user: schemas.UserCreate = Depends(auth.get_current_user)):

    return await user_me(current_user)
