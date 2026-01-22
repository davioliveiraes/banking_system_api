from src.errors.error_types.http_error import HttpError


class HttpUnprocessableEntityError(HttpError):
    def __init__(self, message: str, name: str):
        super().__init__(message=message, name=name, status_code=422)
