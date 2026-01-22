from src.controllers.interfaces.juridica_criar_controller import (
    PessoaJuridicaCriarControllerInterface,
)
from src.errors.error_handler import handle_errors
from src.validators.juridica_criar_validator import juridica_criar_validator

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class PessoaJuridicaCriarViews(ViewInterface):
    def __init__(self, controller: PessoaJuridicaCriarControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            validated_data = juridica_criar_validator(http_request)
            body_response = self.__controller.criar(validated_data)

            return HttpResponse(status_code=201, body=body_response)  # type: ignore

        except Exception as error:
            return handle_errors(error)
