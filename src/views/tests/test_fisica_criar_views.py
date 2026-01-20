from decimal import Decimal
from typing import Dict

from src.controllers.interfaces.fisica_criar_controller import (
    PessoaFisicaCriarControllerInterface,
)
from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.views.fisica_criar_views import PessoaFisicaCriarView
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse


class MockPessoaFisicaCriarController(PessoaFisicaCriarControllerInterface):
    def criar(self, pessoa_data: Dict) -> Dict:
        return {
            "success": True,
            "data": {"type": "Pessoa Física", "count": 1, "attributes": pessoa_data},
        }


class MockPessoaFisicaCriarControllerError(PessoaFisicaCriarControllerInterface):
    def criar(self, pessoa_data: Dict) -> Dict:
        raise HttpBadRequestError("Erro ao criar pessoa física")


def test_handle():
    pessoa_data = {
        "nome_completo": "Jesse Pinkman",
        "email": "jessepinkman@gmail.com",
        "celular": "(88) 9 9120-3123",
        "idade": 27,
        "renda_mensal": Decimal("400000"),
        "categoria": "Vendedor",
        "saldo": Decimal("500000"),
    }

    http_request = HttpRequest(body=pessoa_data)
    controller = MockPessoaFisicaCriarController()
    view = PessoaFisicaCriarView(controller)  # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 201
    assert response.body["data"]["type"] == "Pessoa Física"
    assert response.body["data"]["count"] == 1
    assert response.body["data"]["attributes"] == pessoa_data


def test_handle_with_invalid_data():
    pessoa_data = {
        "nome_completo": "Jesse Pinkman",
        "email": "jessepinkmangmail.com",
        "celular": "(88) 9 9120-3123",
        "idade": 27,
        "renda_mensal": Decimal("400000"),
        "categoria": "Vendedor",
        "saldo": Decimal("500000"),
    }

    http_request = HttpRequest(body=pessoa_data)
    controller = MockPessoaFisicaCriarControllerError()
    view = PessoaFisicaCriarView(controller)  # type: ignore

    response = view.handle(http_request)

    assert response.status_code == 400
    assert response.body == {"success": False, "error": "Erro ao criar pessoa física"}


def test_handle_response_structure():
    pessoa_data = {
        "nome_completo": "Walter White",
        "email": "walterwhite@gmail.com",
        "celular": "(88) 9 1231-2123",
        "idade": 40,
        "renda_mensal": Decimal("4000000"),
        "categoria": "Quimico",
        "saldo": Decimal("5000000"),
    }

    http_request = HttpRequest(body=pessoa_data)
    controller = MockPessoaFisicaCriarController()
    view = PessoaFisicaCriarView(controller)  # type: ignore

    response = view.handle(http_request)

    assert hasattr(response, "status_code")
    assert hasattr(response, "body")
    assert "data" in response.body
    assert "type" in response.body["data"]
    assert "count" in response.body["data"]
    assert "attributes" in response.body["data"]
