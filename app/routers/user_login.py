from fastapi import APIRouter, Query, HTTPException, Depends
from app.models.login import LoginResponse
from app.models.response import ErrorResponse, MessageResponse
from fastapi.security import OAuth2PasswordBearer

from app.services.user_login_service import UserLoginService
from framework.exceptions.response_exceptions import ResponseException

router = APIRouter()

# OAuth2 setup for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=LoginResponse, responses={400: {"model": ErrorResponse}})
async def login(fire_base_token: str = Depends(oauth2_scheme)):
    try:
        user_login_service = UserLoginService()
        response = await user_login_service.login(fire_base_token)
        return response

    except ResponseException as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)

@router.post("/logout", response_model=MessageResponse, responses={401: {"model": ErrorResponse}})
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        user_login_service = UserLoginService()
        message = await user_login_service.logout(token)
        return message

    except ResponseException as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)