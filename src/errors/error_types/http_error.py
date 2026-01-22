class HttpError(Exception):
    def __init__(self, message: str, name: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.name = name
        self.status_code = status_code

    def to_dict(self):
        return {"success": False, "error": self.message}
