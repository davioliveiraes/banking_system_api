from decimal import Decimal
from typing import Dict

from src.controllers.interfaces.fisica_listar_controller import (
    PessoaFisicaListarControllerInterface,
)
from src.views.fisica_listar_views import PessoaFisicaListarViews
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse


class MockPessoaFisicaListarController(PessoaFisicaListarControllerInterface):
    def listar(self) -> Dict:
        return {
            "data": {
                "type": "Pessoa Física",
                "count": 2,
                "attributes": [
                    {
                        "nome_completo": "Jesse Pinkman",
                        "email": "jessepinkman@gmail.com",
                        "celular": "(88) 9 9120-3123",
                        "idade": 27,
                        "renda_mensal": Decimal("400000"),
                        "categoria": "Vendedor",
                        "saldo": Decimal("500000"),
                    },
                    {
                        "nome_completo": "Walter White",
                        "email": "walterwhite@gmail.com",
                        "celular": "(88) 9 1231-2123",
                        "idade": 40,
                        "renda_mensal": Decimal("4000000"),
                        "categoria": "Quimico",
                        "saldo": Decimal("5000000"),
                    },
                ],
            }
        }


class MockPessoaFisicaListaControllerError(PessoaFisicaListarControllerInterface):
    def listar(self) -> Dict:
        raise Exception("Nenhuma Pessoa Física Cadastrada")


def test_handle():
    http_request = HttpRequest(body=None)  # type: ignore
    controller = MockPessoaFisicaListarController()
    view = PessoaFisicaListarViews(controller)

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"]["type"] == "Pessoa Física"
    assert response.body["data"]["count"] == 2
    assert isinstance(response.body["data"]["attributes"], list)


def test_handle_empty_list():
    http_request = HttpRequest(body=None)  # type: ignore
    controller = MockPessoaFisicaListaControllerError()
    view = PessoaFisicaListarViews(controller)

    response = view.handle(http_request)

    assert response.status_code == 400
    assert response.body == {
        "success": False,
        "error": "Nenhuma Pessoa Física Cadastrada",
    }
