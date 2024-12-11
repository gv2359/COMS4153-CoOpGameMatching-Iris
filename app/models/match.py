from pydantic import BaseModel
from typing import List, Dict, Optional
from app.models.pagination_link import PaginationLinks

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

class MatchResponseWithLinks(MatchResponse):
    links: Dict[str, Dict[str, str]]

class MatchResponses(BaseModel):
    matchRequests: List[MatchResponseWithLinks]
    links: PaginationLinks

class MatchStatus(BaseModel):
    matchRequestId: str
    status: str  # Possible values: "matching", "matched", "not_found", "error"
    partnerRequestId: Optional[str] = None

class MatchInitiate(BaseModel):
    MatchRequestId: str

class MatchInitiateResponse(BaseModel):
    message: str
    matchRequestId : str
    polling_url : str