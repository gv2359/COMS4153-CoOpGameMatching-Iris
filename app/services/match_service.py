import os
import httpx

from app.models.match import MatchResponses, MatchRequest, MatchResponse, MatchInitiate, MatchStatus
from app.models.match import MatchResponseWithLinks, MatchInitiateResponse
from app.services.base_validation_service import BaseValidationService
from framework.exceptions.response_exceptions import ResponseException


class MatchService(BaseValidationService):

    def __init__(self):
        self.MATCH_SERVICE_URL = os.getenv("MATCH_SERVICE_URL", "http://localhost:8002")

    @BaseValidationService.validate_token
    async def get_match_request(self, user_id, match_id):
        async with httpx.AsyncClient() as client:
            match_response = await client.get(f"{self.MATCH_SERVICE_URL}/match-requests/{match_id}")
            if match_response.status_code == 200:
                match_responses_model = MatchResponseWithLinks(**match_response.json())
                return match_responses_model
            raise ResponseException(status_code=match_response.status_code, message="Error fetching match request")

    @BaseValidationService.validate_token
    async def get_match_requests(self, user_id, page, page_size, game_id):

        params = {
            "page": page,
            "page_size": page_size,
            "user_id": user_id
        }
        if game_id is not None:
            params["game_id"] = game_id

        async with httpx.AsyncClient() as client:
            match_response = await client.get(f"{self.MATCH_SERVICE_URL}/match-requests", params=params)
            if match_response.status_code == 200:
                match_responses_model = MatchResponses(**match_response.json())
                return match_responses_model
            raise ResponseException(status_code=match_response.status_code, message="Error fetching match requests")

    @BaseValidationService.validate_token
    async def create_match_request(self, user_id, match_request : MatchRequest):

        match_request_data = match_request.dict()
        match_request_data["userId"] = user_id

        game_id = match_request_data["gameId"]

        is_game = await self.validate_game(game_id)
        if not is_game:
            raise ResponseException(status_code=404, message="Game not found")

        async with httpx.AsyncClient() as client:
            match_response = await client.post(f"{self.MATCH_SERVICE_URL}/match-requests", json=match_request_data)

            if match_response.status_code == 201:
                match_response_model = MatchResponse(**match_response.json())
                return match_response_model

            raise ResponseException(status_code=match_response.status_code,
                                message="Error creating match request in the Match service")

    @BaseValidationService.validate_token
    async def initiate_match(self, user_id, match_initiate: MatchInitiate):

        match_id = match_initiate["MatchRequestId"]
        is_valid_match = self.validate_match_request(match_id)

        if not is_valid_match:
            raise ResponseException(status_code=404, message="Match not found or not valid")

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.MATCH_SERVICE_URL}/match-requests/match", json=match_initiate)

            if response.status_code == 202:
                response_model = MatchInitiateResponse(**response.json())
                return response_model

            raise ResponseException(status_code=response.status_code, message="Error initiating matching process")

    @BaseValidationService.validate_token
    async def get_match_status(self, user_id, match_id):

        is_valid_match = await self.validate_match_request(match_id)
        if not is_valid_match:
            raise ResponseException(status_code=404, message="Match not found or not valid")

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.MATCH_SERVICE_URL}/match/status/{match_id}")

            if response.status_code == 200:
                match_status_model = MatchStatus(**response.json())
                return match_status_model

            raise ResponseException(status_code=response.status_code, message="Error finding match status")


    async def validate_game(self, game_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.MATCH_SERVICE_URL}/games/{game_id}")
            if response.status_code == 200:
                return True
            return False

    async def validate_match_request(self, match_request_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.MATCH_SERVICE_URL}/match_requests/{match_request_id}")
            if response.status_code == 200:
                return True
            return False