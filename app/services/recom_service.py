from typing import Any
import os
import httpx

from app.models.recom_models import UserActivityRequest, UserActivityResponse, Recommendations
from app.services.base_validation_service import BaseValidationService
from framework.exceptions.response_exceptions import ResponseException
from framework.resources.base_resource import BaseResource



class RecomService(BaseValidationService):

    def __init__(self):
        self.RECOM_SERVICE_URL = os.getenv("RECOM_SERVICE_URL", "http://localhost:8005")
        self.MATCH_SERVICE_URL = os.getenv("MATCH_SERVICE_URL", "http://localhost:8002")

    @BaseValidationService.validate_token
    async def perform_activity(self, user_id, user_activity: UserActivityRequest) -> UserActivityResponse:

        game_id = user_activity["gameId"]
        is_valid_game = self.validate_game(game_id)
        if not is_valid_game:
            raise ResponseException(status_code=404, message="Game not found")

        user_activity["userId"] = user_id

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.RECOM_SERVICE_URL}/user_activity", json=user_activity)
            if response.status_code == 200:
                user_act_response = UserActivityResponse(**response.json())
                return user_act_response
            raise ResponseException(status_code=response.status_code, message="Error adding user_activity")

    # @BaseValidationService.validate_token
    async def get_recommendations(self, user_id, num_recoms) -> Recommendations:
        params = {
            "num_recoms": num_recoms
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.RECOM_SERVICE_URL}/recommendations/{user_id}", params=params)
            if response.status_code == 200:
                recom_response = Recommendations(**response.json())
                return recom_response
            raise ResponseException(status_code=response.status_code, message="Error fetching recommendations")

    async def validate_game(self, game_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.MATCH_SERVICE_URL}/games/{game_id}")
            if response.status_code == 200:
                return True
            return False
