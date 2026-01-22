from src.controllers.interfaces.fisica_listar_controller import (
    PessoaFisicaListarControllerInterface,
)
from src.errors.error_handler import handle_errors

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class PessoaFisicaListarViews(ViewInterface):
    def __init__(self, controller: PessoaFisicaListarControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body_response = self.__controller.listar()

            return HttpResponse(status_code=200, body=body_response)

        except Exception as error:
            return handle_errors(error)
