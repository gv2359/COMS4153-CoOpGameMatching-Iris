from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.response import ErrorResponse
from app.models.favourite import FavouriteResponse, FavouriteRequest, FavouritesResponse
from app.services.favourites_service import FavouritesService
from framework.exceptions.response_exceptions import ResponseException

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/favourite", response_model=FavouriteResponse,
         responses={201: {"model": FavouriteResponse},401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def add_favourite(favourite_request: FavouriteRequest, token: str = Depends(oauth2_scheme)):
    try:
        favourite_service = FavouritesService()
        favourite_response = await favourite_service.add_favourite(token, favourite_request)
        return favourite_response

    except ResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/favourites", response_model=FavouritesResponse,
         responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_favourites(page: int = 1,page_size: int = 5, token: str = Depends(oauth2_scheme)):
    try:
        games_service = FavouritesService()
        games_response = await games_service.get_favourites(token, page, page_size)
        return games_response

    except ResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
