import os
import httpx

from app.services.base_validation_service import BaseValidationService
from framework.exceptions.response_exceptions import ResponseException
from app.models.login import LoginResponse
from app.models.response import MessageResponse


class UserLoginService(BaseValidationService):

    def __init__(self):
        super().__init__()
        self.USER_VALIDATION_SERVICE_URL = os.getenv("USER_VALIDATION_SERVICE_URL", "http://localhost:8001")


    async def login(self, access_token):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.USER_VALIDATION_SERVICE_URL}/login-google", headers={"Authorization": f"Bearer {access_token}"})
                if response.status_code == 200:
                    return LoginResponse(**response.json())  # Use the new response model
                raise ResponseException(status_code=response.status_code, message=response.json().get("detail", "Login failed"))
        except Exception as e:
            raise ResponseException(status_code=500, message=f"Service error : {str(e)}")

    async def logout(self,token):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.USER_VALIDATION_SERVICE_URL}/logout",headers={"Authorization": f"Bearer {token}"})
                if response.status_code == 200:
                    message_response = MessageResponse(message = "Successfully logged out")
                    return message_response
                else:
                    raise ResponseException(status_code=response.status_code, message = response.json().get("detail", "Logout failed"))
        except Exception as e:
            print(e)
            raise ResponseException(status_code=500, message=f"Service Error : {str(e)}")