from src.errors.error_types.http_error import HttpError


class HttpBadRequestError(HttpError):
    def __init__(self, message: str, name: str):
        super().__init__(message=message, name=name, status_code=400)
