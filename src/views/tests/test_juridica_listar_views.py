from decimal import Decimal
from typing import Dict

from src.controllers.interfaces.juridica_listar_controller import (
    PessoaJuridicaListarControllerInterface,
)
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.juridica_listar_views import PessoaJuridicaListaView


class MockPessoaJuridicaListarController(PessoaJuridicaListarControllerInterface):
    def listar(self) -> Dict:
        return {
            "data": {
                "type": "Pessoa Jurídica",
                "count": 2,
                "attributes": [
                    {
                        "nome_fantasia": "Vivo Keyd Stars",
                        "email_corporativo": "vivokeydstars@gmail.com",
                        "celular": "(55) 9 0808-2112",
                        "categoria": "League of Legends",
                        "faturamento": Decimal("590000"),
                        "idade": 8,
                        "saldo": Decimal("1100000"),
                    },
                    {
                        "nome_fantasia": "LOUD",
                        "email_corporativo": "loud@gmail.com",
                        "celular": "(55) 9 0882-1232",
                        "categoria": "League of Legends",
                        "faturamento": Decimal("580000"),
                        "idade": 8,
                        "saldo": Decimal("1070000"),
                    },
                ],
            }
        }


class MockPessoaJuridicaListarControllerError(PessoaJuridicaListarControllerInterface):
    def listar(self) -> Dict:
        raise HttpNotFoundError("Nenhuma Pessoa Jurídica Encontrada")


def test_handle():
    http_request = HttpRequest(body=None)  # type: ignore
    controller = MockPessoaJuridicaListarController()
    view = PessoaJuridicaListaView(controller)

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"]["type"] == "Pessoa Jurídica"
    assert response.body["data"]["count"] == 2
    assert isinstance(response.body["data"]["attributes"], list)


def test_handle_empty_list():
    http_request = HttpRequest(body=None)  # type: ignore
    controller = MockPessoaJuridicaListarControllerError()
    view = PessoaJuridicaListaView(controller)

    response = view.handle(http_request)

    assert response.status_code == 404
    assert response.body == {
        "success": False,
        "error": "Nenhuma Pessoa Jurídica Encontrada",
    }
