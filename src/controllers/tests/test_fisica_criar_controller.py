from decimal import Decimal
from typing import Dict

from src.controllers.fisica_criar_controller import PessoaFisicaCriarController


class MockPessoaFisica:
    def __init__(self, data):
        self.id = 1
        self.nome_completo = data["nome_completo"]
        self.email = data["email"]
        self.celular = data["celular"]
        self.idade = data["idade"]
        self.renda_mensal = data["renda_mensal"]
        self.categoria = data["categoria"]
        self.saldo = data["saldo"]
        self.criado_em = None
        self.atualizado_em = None


class MockPessoaFisicaRepository:
    def criar_pessoa(self, pessoa_data: Dict):
        return MockPessoaFisica(pessoa_data)


def test_criar_sucesso():
    pessoa_data = {
        "nome_completo": "Dr. Shaun Murphy",
        "email": "shaunmurphy@gmail.com",
        "celular": "11987654321",
        "idade": 25,
        "renda_mensal": Decimal("250000"),
        "categoria": "A",
        "saldo": Decimal("45000000"),
    }

    controller = PessoaFisicaCriarController(MockPessoaFisicaRepository())  # type: ignore
    response = controller.criar(pessoa_data)

    assert response["success"] is True
    assert response["data"]["type"] == "Pessoa Física"
    assert response["data"]["count"] == 1
    attributes = response["data"]["attributes"]
    assert attributes["nome_completo"] == pessoa_data["nome_completo"]
    assert attributes["email"] == pessoa_data["email"]
    assert attributes["celular"] == pessoa_data["celular"]
    assert attributes["idade"] == pessoa_data["idade"]
    assert attributes["renda_mensal"] == float(pessoa_data["renda_mensal"])
    assert attributes["categoria"] == pessoa_data["categoria"]
    assert attributes["saldo"] == float(pessoa_data["saldo"])
    assert attributes["id"] == 1
    assert attributes["criado_em"] is None
    assert attributes["atualizado_em"] is None


def test_criar_error():
    pessoa_data = {
        "nome_completo": "Dr. Shaun Murphy",
        "email": "shaunmurphy@gmail",
        "celular": "4356-1233",
        "idade": 25,
        "renda_mensal": Decimal("250000"),
        "categoria": "A",
        "saldo": Decimal("45000000"),
    }

    controller = PessoaFisicaCriarController(MockPessoaFisicaRepository())  # type: ignore

    response = controller.criar(pessoa_data)
    assert response["success"] is False
    assert "error" in response
