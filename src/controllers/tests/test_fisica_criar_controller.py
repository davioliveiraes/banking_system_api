from decimal import Decimal

from src.controllers.fisica_criar_controller import PessoaCriarController


class MockPessoaFisicaRepository:
    def criar_pessoa(self, pessoa_data: dict):
        return pessoa_data


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

    controller = PessoaCriarController(MockPessoaFisicaRepository())  # type: ignore
    response = controller.criar(pessoa_data)

    assert response["success"] is True
    assert response["data"]["type"] == "Pessoa Física"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == pessoa_data


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

    controller = PessoaCriarController(MockPessoaFisicaRepository())  # type: ignore

    response = controller.criar(pessoa_data)
    assert response["success"] is False
    assert "error" in response
