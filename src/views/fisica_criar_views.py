from src.controllers.interfaces.fisica_criar_controller import (
    PessoaFisicaCriarControllerInterface,
)

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class PessoaFisicaCriarView(ViewInterface):
    def __init__(self, controller: PessoaFisicaCriarControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            pessoa_data = http_request.body
            body_response = self.__controller.criar(pessoa_data)

            return HttpResponse(status_code=201, body=body_response)  # type: ignore
        except Exception as exc:
            return HttpResponse(status_code=400, body={"success": False, "error": str(exc)})  # type: ignore
