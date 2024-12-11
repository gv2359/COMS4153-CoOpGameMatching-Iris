import os

class BaseService:

    def __init__(self):
        self.USER_VALIDATION_SERVICE_URL = os.getenv("USER_VALIDATION_SERVICE_URL", "http://localhost:8001")

    def validate_token(self, func):
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)
            print("Common Cleanup Code")
            return result

        return wrapper

    @classmethod
    @abstractmethod
    def get_service(cls, service_name):
        raise NotImplementedError()