from decimal import Decimal

from src.controllers.fisica_listar_controller import PessoaFisicaListarController


class MockPessoaFisica:
    def __init__(
        self, nome_completo, email, celular, idade, renda_mensal, categoria, saldo
    ) -> None:
        self.nome_completo = nome_completo
        self.email = email
        self.celular = celular
        self.idade = idade
        self.renda_mensal = renda_mensal
        self.categoria = categoria
        self.saldo = saldo


class MockPessoaFisicaRepository:
    def buscar_por_id(self, pessoa_fisica_id: int):
        if pessoa_fisica_id == 123:
            return MockPessoaFisica(
                nome_completo="Nicholas Gonzale",
                email="nicholasgonzale@gmail.com",
                celular="88890123121",
                idade=30,
                renda_mensal=Decimal("400000"),
                categoria="S",
                saldo=Decimal("2000000"),
            )
        return None


def test_listar_sucesso():
    controller = PessoaFisicaListarController(MockPessoaFisicaRepository())  # type: ignore
    response = controller.listar(123)

    expected_response = {
        "data": {
            "type": "Pessoa Física",
            "count": 1,
            "attributes": {
                "nome_completo": "Nicholas Gonzale",
                "email": "nicholasgonzale@gmail.com",
                "celular": "88890123121",
                "idade": 30,
                "renda_mensal": Decimal("400000"),
                "categoria": "S",
                "saldo": Decimal("2000000"),
            },
        }
    }

    assert response == expected_response


def test_listar_nao_encontrado():
    controller = PessoaFisicaListarController(MockPessoaFisicaRepository())  # type: ignore

    response = controller.listar(999)
    assert response["success"] is False
    assert "error" in response
