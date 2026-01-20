from src.controllers.interfaces.juridica_listar_controller import (
    PessoaJuridicaListarControllerInterface,
)
from src.errors.error_types.http_error import HttpError

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

        except HttpError as error:
            return HttpResponse(status_code=error.status_code, body=error.to_dict())

        except Exception as exc:
            return HttpResponse(
                status_code=500,
                body={
                    "success": False,
                    "error": f"Erro interno do servidor: {str(exc)}",
                },
            )
