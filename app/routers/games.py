from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from app.models.game import GameResponse, GamesResponse
from app.models.response import ErrorResponse
from fastapi.security import OAuth2PasswordBearer

from app.services.games_service import GamesService
from app.services.user_login_service import UserLoginService
from framework.exceptions.response_exceptions import ResponseException

router = APIRouter()

# OAuth2 setup for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/games/{game_id}", response_model=GameResponse,
            responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def games(game_id: Optional[str] = None,
                token: str = Depends(oauth2_scheme)):
    try:
        games_service = GamesService()
        games_response = await games_service.get_game(token, game_id)
        return games_response

    except ResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/games", response_model=GamesResponse,
         responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def games(
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        game_id: Optional[str] = None,
        genre : Optional[str] = None,
        token: str = Depends(oauth2_scheme)
):
    try:
        games_service = GamesService()
        games_response = await games_service.get_games(token, page, page_size, title, game_id, genre)
        return games_response

    except ResponseException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.message)




