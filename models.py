from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
import uuid

class UserRegister(BaseModel):
    userName: str
    emailId: EmailStr
    password: str

class UserLogin(BaseModel):
    emailId: EmailStr
    password: str

class Game(BaseModel):
    gameId: str
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    genre: Optional[str] = None

class GameWithLinks(Game):
    links: Dict[str, Dict[str, str]]

class PaginationLinks(BaseModel):
    self: Dict[str, str]
    next: Optional[Dict[str, str]] = None
    prev: Optional[Dict[str, str]] = None

class GamesResponse(BaseModel):
    games: List[GameWithLinks]
    links: PaginationLinks

class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class MatchRequest(BaseModel):
    gameId: str
    expireDate: str  # Use str for date or adjust to use a specific date type
    isActive: bool = False
    isCancelled: bool = False

class MatchResponse(BaseModel):
    userId: str
    gameId: str
    matchRequestId: str
    expireDate: str
    isActive: bool
    isCancelled: bool

class MatchRequestWithLinks(MatchRequest):
    links: Dict[str, Dict[str, str]]

class MatchRequestResponse(BaseModel):
    matchRequests: List[MatchRequestWithLinks]
    links: PaginationLinks