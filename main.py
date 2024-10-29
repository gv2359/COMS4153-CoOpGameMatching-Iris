# main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Optional
import httpx
import os
from dotenv import load_dotenv
import jwt
from models import (
    MatchRequestResponse,
    UserRegister, 
    UserLogin, 
    GamesResponse, 
    MessageResponse, 
    ErrorResponse,
    LoginResponse,
    MatchRequest,
    MatchResponse
)

load_dotenv()

# Configuration for services
USER_VALIDATION_SERVICE_URL = os.getenv("USER_VALIDATION_SERVICE_URL", "http://localhost:8001")
MATCH_SERVICE_URL = os.getenv("MATCH_SERVICE_URL", "http://localhost:8002")

app = FastAPI()

# OAuth2 setup for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# API Endpoints
@app.post("/register", response_model=MessageResponse, responses={400: {"model": ErrorResponse}})
async def register(user: UserRegister):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_VALIDATION_SERVICE_URL}/register", json=user.dict())
        if response.status_code == 200:
            return {"message": "User registered successfully"}
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Registration failed"))

@app.post("/login", response_model=LoginResponse, responses={400: {"model": ErrorResponse}})
async def login(user: UserLogin):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_VALIDATION_SERVICE_URL}/login", json=user.dict())
        if response.status_code == 200:
            return LoginResponse(**response.json())  # Use the new response model
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Login failed"))

@app.post("/logout", response_model=MessageResponse, responses={401: {"model": ErrorResponse}})
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{USER_VALIDATION_SERVICE_URL}/logout", headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                return {"message": "Successfully logged out"}
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Logout failed"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/games", response_model=GamesResponse, responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def games(
    page: int = 1,
    page_size: int = 10,
    title: Optional[str] = None,
    gameId: Optional[str] = None,
    token: str = Depends(oauth2_scheme)
):
    # Validate token by calling UserValidationService
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_VALIDATION_SERVICE_URL}/validate-token", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Invalid or expired token")
    
    # Forward the request to the Match service if token is valid
    async with httpx.AsyncClient() as client:
        match_response = await client.get(
            f"{MATCH_SERVICE_URL}/games",
            headers={"Authorization": f"Bearer {token}"},
            params={"page": page, "page_size": page_size, "title": title, "gameId": gameId}
        )
        if match_response.status_code == 200:
            return match_response.json()
        raise HTTPException(status_code=match_response.status_code, detail="Error fetching games")

@app.get("/match-requests", response_model=MatchRequestResponse, responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def match_requests(
    page: int = 1,
    page_size: int = 10,
    gameId: Optional[str] = None,
    token: str = Depends(oauth2_scheme)
):
    # Validate token by calling UserValidationService
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_VALIDATION_SERVICE_URL}/validate-token", headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Invalid or expired token")
    
    # Extract user information from the validation response
    user_info = response.json()
    user_id = user_info.get("user_id")
    
    # Forward the request to the Match service if token is valid
    async with httpx.AsyncClient() as client:
        match_response = await client.get(
            f"{MATCH_SERVICE_URL}/match-requests",
            headers={"Authorization": f"Bearer {token}"},
            params={"page": page, "page_size": page_size, "userId": user_id, "gameId": gameId}
        )
        if match_response.status_code == 200:
            return match_response.json()
        raise HTTPException(status_code=match_response.status_code, detail="Error fetching games")

@app.post("/match-requests", responses={201: {"model": MatchResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def create_match_request(
    match_request: MatchRequest,
    token: str = Depends(oauth2_scheme)
):
    async with httpx.AsyncClient() as client:
        validate_response = await client.post(
            f"{USER_VALIDATION_SERVICE_URL}/validate-token", 
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if validate_response.status_code != 200:
            raise HTTPException(status_code=validate_response.status_code, detail="Invalid or expired token")

        # Extract user information from the validation response
        user_info = validate_response.json()
        user_id = user_info.get("user_id")
        
        # Add userId to the match request data
        match_request_data = match_request.dict()
        match_request_data["userId"] = user_id 

        # Forward the request to the Match service with the userId included
        async with httpx.AsyncClient() as client:
            match_response = await client.post(
                f"{MATCH_SERVICE_URL}/match-requests",
                json=match_request_data,
                headers={"Authorization": f"Bearer {token}"},
            )

            if match_response.status_code == 201:
                return match_response.json()

            raise HTTPException(status_code=match_response.status_code, detail="Error creating match request in the Match service")

@app.get("/health", response_model=MessageResponse)
async def health_check():
    return {"message": "Iris Gateway is running"}