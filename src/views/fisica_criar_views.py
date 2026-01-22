from src.controllers.interfaces.fisica_criar_controller import (
    PessoaFisicaCriarControllerInterface,
)
from src.errors.error_handler import handle_errors
from src.validators.fisica_criar_validator import fisica_criar_validator

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class PessoaFisicaCriarView(ViewInterface):
    def __init__(self, controller: PessoaFisicaCriarControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            validated_data = fisica_criar_validator(http_request)
            body_response = self.__controller.criar(validated_data)
            return HttpResponse(status_code=201, body=body_response)  # type: ignore

        except Exception as error:
            return handle_errors(error)
