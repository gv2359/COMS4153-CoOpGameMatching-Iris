from typing import List
from pydantic import BaseModel
from app.models.game import GameResponse

class FavouriteRequest(BaseModel):
    gameId: str

class FavouriteResponse(BaseModel):
    favouriteId: str
    userId: str
    gameId: str

class FavouritesResponse(BaseModel):
    games: List[GameResponse]