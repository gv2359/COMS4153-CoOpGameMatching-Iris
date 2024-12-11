import os
import httpx
from app.models.game import GameResponse, GamesResponse
from app.services.base_validation_service import BaseValidationService
from framework.exceptions.response_exceptions import ResponseException


class GamesService(BaseValidationService):

    def __init__(self):
        self.MATCH_SERVICE_URL = os.getenv("MATCH_SERVICE_URL", "http://localhost:8002")

    @BaseValidationService.validate_token
    async def get_game(self, user_id, game_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.MATCH_SERVICE_URL}/games/{game_id}")
            if response.status_code == 200:
                game_response = GameResponse(**response.json())
                return game_response
            raise ResponseException(status_code=response.status_code, message="Error fetching game")

    @BaseValidationService.validate_token
    async def get_games(self, user_id, page, page_size, title, game_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.MATCH_SERVICE_URL}/games",
                params={"page": page, "page_size": page_size, "title": title, "gameId": game_id}
            )
            if response.status_code == 200:
                games_response = GamesResponse(**response.json())
                return games_response
            raise ResponseException(status_code=response.status_code, message="Error fetching games")



