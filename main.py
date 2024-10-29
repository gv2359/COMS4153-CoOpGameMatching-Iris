from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional, Dict
import httpx
import os
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
import jwt

load_dotenv()

# Configuration for UserValidationService
USER_VALIDATION_SERVICE_URL = os.getenv("USER_VALIDATION_SERVICE_URL", "http://localhost:8001")
MATCH_SERVICE_URL = os.getenv("MATCH_SERVICE_URL", "http://localhost:8002")

app = FastAPI()

# OAuth2 setup for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic Models for structured responses and requests
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
    next: Optional[Dict[str, str]]
    prev: Optional[Dict[str, str]]

class GamesResponse(BaseModel):
    games: List[GameWithLinks]
    links: PaginationLinks

# Enhanced response models
class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str

# API Endpoints
@app.post("/register", response_model=MessageResponse, responses={400: {"model": ErrorResponse}})
async def register(user: UserRegister):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_VALIDATION_SERVICE_URL}/register", json=user.dict())
        if response.status_code == 200:
            return {"message": "User registered successfully"}
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Registration failed"))

@app.post("/login", response_model=Dict[str, str], responses={400: {"model": ErrorResponse}})
async def login(user: UserLogin):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_VALIDATION_SERVICE_URL}/login", json=user.dict())
        if response.status_code == 200:
            return response.json()
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

@app.get("/health", response_model=MessageResponse)
async def health_check():
    return {"message": "Iris Gateway is running"}
