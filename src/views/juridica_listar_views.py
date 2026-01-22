from src.controllers.interfaces.juridica_listar_controller import (
    PessoaJuridicaListarControllerInterface,
)
from src.errors.error_handler import handle_errors

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class PessoaJuridicaListaView(ViewInterface):
    def __init__(self, controller: PessoaJuridicaListarControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body_response = self.__controller.listar()

            return HttpResponse(status_code=200, body=body_response)  # type: ignore

        except Exception as error:
            return handle_errors(error)
