from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.models.match import MatchRequest, MatchResponses, MatchResponseWithLinks, MatchStatus
from app.models.match import MatchInitiate, MatchResponse, MatchInitiateResponse
from app.models.response import ErrorResponse
from app.services.match_service import MatchService
from framework.exceptions.response_exceptions import ResponseException

router = APIRouter()

# OAuth2 setup for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/match-requests/{match_request_id}", response_model=MatchResponseWithLinks,
         responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def match_requests(match_request_id: str, token: str = Depends(oauth2_scheme)):
    try:
        match_service = MatchService()
        match_response = await match_service.get_match_request(token, match_request_id)
        return match_response
    except ResponseException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/match-requests", response_model=MatchResponses,
         responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def match_requests(
        page: int = 1,
        page_size: int = 10,
        game_id: Optional[str] = None,
        token: str = Depends(oauth2_scheme)
):
    try:
        match_service = MatchService()
        match_responses = await match_service.get_match_requests(token, page, page_size, game_id)
        return match_responses
    except ResponseException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/match-requests", response_model=MatchResponse,
         responses={201: {"model": MatchResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def match_requests(match_request: MatchRequest, token: str = Depends(oauth2_scheme)):
    try:
        match_service = MatchService()
        match_response = await match_service.create_match_request(token, match_request)
        return match_response
    except ResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/match-requests/match", response_model=MatchInitiateResponse,
             responses = {202: {"model":MatchInitiateResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def initiate_match(match_request_initiate: MatchInitiate, token: str = Depends(oauth2_scheme) ):
    try:
        match_service = MatchService()
        match_responses = await match_service.initiate_match(token, match_request_initiate)
        return match_responses
    except ResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/match/status/{match_request_id}", response_model=MatchStatus)
async def get_matchmaking_status(match_request_id: str, token: str = Depends(oauth2_scheme)):
    try:
        match_service = MatchService()
        match_responses = await match_service.get_match_status(token, match_request_id)
        return match_responses
    except ResponseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)