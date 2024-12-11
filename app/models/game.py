from typing import Optional, Dict, List
from pydantic import BaseModel
from app.models.pagination_link import PaginationLinks

class GameResponse(BaseModel):
    gameId: str
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    genre: Optional[str] = None
    links: Optional[Dict[str, Dict[str, str]]]

class GamesResponse(BaseModel):
    games: List[GameResponse]
    links: PaginationLinks