import os
import httpx

from app.models.favourite import FavouriteResponse, FavouriteRequest, FavouritesResponse
from app.services.base_validation_service import BaseValidationService
from framework.exceptions.response_exceptions import ResponseException


class FavouritesService(BaseValidationService):

    def __init__(self):
        self.MATCH_SERVICE_URL = os.getenv("MATCH_SERVICE_URL", "http://localhost:8002")

    @BaseValidationService.validate_token
    async def add_favourite(self, user_id, favourite_request:FavouriteRequest) -> FavouriteResponse:

        game_id = favourite_request["gameId"]
        is_valid_game = self.validate_game(game_id)
        if not is_valid_game:
            raise ResponseException(status_code=404, message="Game not found")

        favourite_request["userId"] = user_id

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.MATCH_SERVICE_URL}/favourite", json=favourite_request)
            if response.status_code == 200:
                fav_response = FavouriteResponse(**response.json())
                return fav_response
            raise ResponseException(status_code=response.status_code, message="Error adding favourite game")

    @BaseValidationService.validate_token
    async def get_favourites(self, user_id, page, page_size) -> FavouritesResponse:
        params = {
            "page": page,
            "page_size": page_size,
            "user_id": user_id
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.MATCH_SERVICE_URL}/favourites/{user_id}", params=params)
            if response.status_code == 200:
                favs_response = FavouritesResponse(**response.json())
                return favs_response
            raise ResponseException(status_code=response.status_code, message="Error adding favourite game")

    async def validate_game(self, game_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.MATCH_SERVICE_URL}/games/{game_id}")
            if response.status_code == 200:
                return True
            return False
