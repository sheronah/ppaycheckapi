from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from modules.user_L import sign_up, login, user_me
from middleware.tokensHashes import TokenWorks, PasswordWorks
from models.users_M import User, Auth, Token, UserX

router = APIRouter()


@router.post("/signup")
async def create_user(user: UserX):
    return await sign_up(user)


@router.post("/login")
async def login_for_access_token(form_data: Auth):
    return await login(form_data)


@router.get("/users/me")
async def read_users_me(current_user: int = Depends(TokenWorks.verify_token)):
    return await user_me(current_user)
