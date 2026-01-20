from decimal import Decimal

import pytest

from src.controllers.fisica_listar_controller import PessoaFisicaListarController
from src.errors.error_types.http_not_found import HttpNotFoundError


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
    def __init__(self, retornar_vazio=False):
        self.retornar_vazio = retornar_vazio

    def listar_todas(self):
        if self.retornar_vazio:
            return []

        return [
            MockPessoaFisica(
                nome_completo="Nicholas Gonzale",
                email="nicholasgonzale@gmail.com",
                celular="88890123121",
                idade=30,
                renda_mensal=Decimal("400000"),
                categoria="S",
                saldo=Decimal("2000000"),
            )
        ]


def test_listar_sucesso():
    controller = PessoaFisicaListarController(MockPessoaFisicaRepository(retornar_vazio=False))  # type: ignore

    response = controller.listar()

    expected_response = {
        "data": {
            "type": "Pessoa Física",
            "count": 1,
            "attributes": [
                {
                    "nome_completo": "Nicholas Gonzale",
                    "email": "nicholasgonzale@gmail.com",
                    "celular": "88890123121",
                    "idade": 30,
                    "renda_mensal": Decimal("400000"),
                    "categoria": "S",
                    "saldo": Decimal("2000000"),
                },
            ],
        }
    }

    assert response == expected_response


def test_listar_nao_encontrado():
    controller = PessoaFisicaListarController(MockPessoaFisicaRepository(retornar_vazio=True))  # type: ignore

    with pytest.raises(HttpNotFoundError) as exc_info:
        controller.listar()

    assert "Nenhuma Pessoa Física Cadastrada" in str(exc_info.value)


def test_listar_multiplas_pessoas():
    class MockRepositoryMultiplo:
        def listar_todas(self):
            return [
                MockPessoaFisica(
                    nome_completo="Dr. Neil Melendez",
                    email="neilmelendez@gmail.com",
                    celular="88987311031",
                    idade=30,
                    renda_mensal=Decimal("400000"),
                    categoria="S",
                    saldo=Decimal("2000000"),
                ),
                MockPessoaFisica(
                    nome_completo="Dr.ª Claire Browne",
                    email="clairebrowne.com",
                    celular="88989101112",
                    idade=27,
                    renda_mensal=Decimal("300000"),
                    categoria="A",
                    saldo=Decimal("1000000"),
                ),
            ]

    controller = PessoaFisicaListarController(MockRepositoryMultiplo())  # type: ignore
    response = controller.listar()

    assert response["data"]["count"] == 2
    assert len(response["data"]["attributes"]) == 2
    assert response["data"]["attributes"][0]["nome_completo"] == "Dr. Neil Melendez"
    assert response["data"]["attributes"][1]["nome_completo"] == "Dr.ª Claire Browne"
