import os
import httpx
from framework.exceptions.response_exceptions import ResponseException

class BaseValidationService:

    @staticmethod
    def validate_token(func):
        async def validate(token, *args, **kwargs):
            try:
                async with httpx.AsyncClient() as client:
                    user_validation_service_url = os.getenv("USER_VALIDATION_SERVICE_URL", "http://localhost:8001")
                    response = await client.post(f"{user_validation_service_url}/validate-token",
                                                 headers={"Authorization": f"Bearer {token}"})
                    if response.status_code == 200:
                        user_info = response.json()
                        user_id = user_info.get("user_id")
                        return await func(user_id, *args, **kwargs)
                    else:
                        raise ResponseException(status_code=response.status_code,
                                                message=response.json().get("detail", "Access Denied"))
            except Exception as e:
                raise ResponseException(status_code=500,message=f"Service Error : {e}")
        return validate