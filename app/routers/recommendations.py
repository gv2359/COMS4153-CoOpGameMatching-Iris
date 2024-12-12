from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.recom_models import Recommendations, UserActivityResponse, UserActivityRequest
from app.models.response import ErrorResponse
from app.services.recom_service import RecomService
from framework.exceptions.response_exceptions import ResponseException

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/user_activity", response_model=UserActivityResponse,
         responses={201: {"model": UserActivityResponse},401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def mark_activity(user_activity_request: UserActivityRequest, token: str = Depends(oauth2_scheme)):
    try:
        favourite_service = RecomService()
        favourite_response = await favourite_service.perform_activity(token, user_activity_request)
        return favourite_response

    except ResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/recommendations", response_model=Recommendations,
         responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_recommendations(num_recoms: int = 6, token: str = Depends(oauth2_scheme)):
    try:
        recom_service = RecomService()
        recoms_response = await recom_service.get_recommendations(token, num_recoms)
        return recoms_response

    except ResponseException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.message)
