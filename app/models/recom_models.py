from app.models.game import GameResponse
from typing import List
from pydantic import BaseModel

class Recommendations(BaseModel):
    userId: str
    games: List[GameResponse]

class UserActivityRequest(BaseModel):
    gameId: str
    isMatched: bool
    isInterested: bool

class UserActivityResponse(BaseModel):
    userId: str
    gameId: str
    isMatched: bool
    isInterested: bool