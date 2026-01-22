from decimal import Decimal
from typing import Dict

from src.controllers.interfaces.juridica_criar_controller import (
    PessoaJuridicaCriarControllerInterface,
)
from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse
from src.views.juridica_criar_views import PessoaJuridicaCriarViews


class MockPessoaJuridicaCriarController(PessoaJuridicaCriarControllerInterface):
    def criar(self, pessoa_data: Dict) -> Dict:
        return {
            "success": True,
            "data": {"type": "Pessoa Jurídica", "count": 1, "attributes": pessoa_data},
        }


class MockPessoaJuridicaCriarControllerError(PessoaJuridicaCriarControllerInterface):
    def criar(self, pessoa_data: Dict) -> Dict:
        raise HttpBadRequestError(
            message="Erro ao criar pessoa jurídica", name="Bad Request"
        )


def test_handle():
    pessoa_data = {
        "nome_fantasia": "RED Canids Kalunga",
        "email_corporativo": "redcanidskalunga@gmail.com",
        "celular": "(55) 9 3120-2131",
        "categoria": "League of Legends",
        "faturamento": Decimal("560000"),
        "idade": 8,
        "saldo": Decimal("1000000"),
    }

    http_request = HttpRequest(body=pessoa_data)
    controller = MockPessoaJuridicaCriarController()
    view = PessoaJuridicaCriarViews(controller)

    response = view.handle(http_request)

    assert (
        response.body["data"]["attributes"]["nome_fantasia"]
        == pessoa_data["nome_fantasia"]
    )
    assert (
        response.body["data"]["attributes"]["email_corporativo"]
        == pessoa_data["email_corporativo"]
    )


def test_handle_with_invalid_data():
    pessoa_data = {
        "nome_fantasia": "RED Canids Kalunga",
        "email_corporativo": "redcanidskalunga@gmail.com",
        "celular": "(55) 9 3120-2131",
        "categoria": "League of Legends",
        "faturamento": Decimal("560000"),
        "idade": 8,
        "saldo": Decimal("1000000"),
    }

    http_request = HttpRequest(body=pessoa_data)
    controller = MockPessoaJuridicaCriarControllerError()
    view = PessoaJuridicaCriarViews(controller)

    response = view.handle(http_request)

    assert response.status_code == 400
    assert response.body == {
        "errors": [{"title": "Bad Request", "detail": "Erro ao criar pessoa jurídica"}]
    }


def test_handle_response_structure():
    pessoa_data = {
        "nome_fantasia": "paiN Gaming",
        "email_corporativo": "paingaming@gmail.com",
        "celular": "(55) 9 1232-1232",
        "categoria": "League of Legends",
        "faturamento": Decimal("570000"),
        "idade": 8,
        "saldo": Decimal("1200000"),
    }

    http_request = HttpRequest(body=pessoa_data)
    controller = MockPessoaJuridicaCriarController()
    view = PessoaJuridicaCriarViews(controller)

    response = view.handle(http_request)

    assert hasattr(response, "status_code")
    assert hasattr(response, "body")
    assert "data" in response.body
    assert "type" in response.body["data"]
    assert "count" in response.body["data"]
    assert "attributes" in response.body["data"]
