
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routers import games, match_requests, favourites, user_login, recommendations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# it loads from the .env file
load_dotenv()

app.include_router(user_login.router)
app.include_router(games.router)
app.include_router(match_requests.router)
app.include_router(favourites.router)
app.include_router(recommendations.router)

@app.get("/health")
async def health():
    return {"message": "Service is up and running"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
