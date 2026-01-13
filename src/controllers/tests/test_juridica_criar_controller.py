from decimal import Decimal
from typing import Dict

from src.controllers.juridica_criar_controller import PessoaJuridicaCriarControler


class MockPessoaJuridicaRepository:
    def criar_empresa(self, pessoa_data: Dict):
        return pessoa_data


def test_criar_sucesso():
    pessoa_data = {
        "nome_fantasia": "Hospital Israelita Albert Einstein",
        "email_corporativo": "hospitaliaeinstein@gmail.com",
        "celular": "55232131231",
        "idade": 20,
        "faturamento": Decimal("15000000"),
        "categoria": "Saúde",
        "saldo": Decimal("250000000"),
    }

    controller = PessoaJuridicaCriarControler(MockPessoaJuridicaRepository())  # type: ignore
    response = controller.criar(pessoa_data)

    assert response["success"] is True
    assert response["data"]["type"] == "Pessoa Jurídica"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == pessoa_data


def test_criar_error():
    pessoa_data = {
        "nome_fantasia": "Hospital Israelita Albert Einstein",
        "email_corporativo": "hospitaliaeinsteingmail.com",
        "celular": "55232131231",
        "idade": 20,
        "faturamento": Decimal("15000000"),
        "categoria": "Saúde",
        "saldo": Decimal("250000000"),
    }

    controller = PessoaJuridicaCriarControler(MockPessoaJuridicaRepository())  # type: ignore

    response = controller.criar(pessoa_data)
    assert response["success"] is False
    assert "error" in response
