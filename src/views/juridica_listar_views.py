from src.controllers.interfaces.juridica_listar_controller import (
    PessoaJuridicaListarControllerInterface,
)

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
        except Exception as exc:
            return HttpResponse(
                status_code=400, body={"success": False, "error": str(exc)}
            )
