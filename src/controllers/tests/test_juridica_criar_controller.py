from decimal import Decimal
from typing import Dict

from src.controllers.juridica_criar_controller import PessoaJuridicaCriarControler


class MockPessoaJuridica:
    def __init__(self, data):
        self.id = 1
        self.nome_fantasia = data["nome_fantasia"]
        self.email_corporativo = data["email_corporativo"]
        self.celular = data["celular"]
        self.idade = data["idade"]
        self.faturamento = data["faturamento"]
        self.categoria = data["categoria"]
        self.saldo = data["saldo"]
        self.criado_em = None
        self.atualizado_em = None


class MockPessoaJuridicaRepository:
    def criar_empresa(self, pessoa_data: Dict):
        return MockPessoaJuridica(pessoa_data)


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
    attributes = response["data"]["attributes"]
    assert attributes["nome_fantasia"] == pessoa_data["nome_fantasia"]
    assert attributes["email_corporativo"] == pessoa_data["email_corporativo"]
    assert attributes["celular"] == pessoa_data["celular"]
    assert attributes["idade"] == pessoa_data["idade"]
    assert attributes["faturamento"] == float(pessoa_data["faturamento"])
    assert attributes["categoria"] == pessoa_data["categoria"]
    assert attributes["saldo"] == float(pessoa_data["saldo"])
    assert attributes["id"] == 1
    assert attributes["criado_em"] is None
    assert attributes["atualizado_em"] is None


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
