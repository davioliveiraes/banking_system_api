from decimal import Decimal

import pytest

from src.controllers.juridica_listar_controller import PessoaJuridicaListarController
from src.errors.error_types.http_not_found import HttpNotFoundError


class MockPessoaJuridica:
    def __init__(
        self,
        nome_fantasia,
        email_corporativo,
        celular,
        idade,
        faturamento,
        categoria,
        saldo,
    ):
        self.nome_fantasia = nome_fantasia
        self.email_corporativo = email_corporativo
        self.celular = celular
        self.idade = idade
        self.faturamento = faturamento
        self.categoria = categoria
        self.saldo = saldo


class MockPessoaJuridicaRepository:
    def __init__(self, retornar_vazio=False):
        self.retornar_vazio = retornar_vazio

    def listar_todas(self):
        if self.retornar_vazio:
            return []

        return [
            MockPessoaJuridica(
                nome_fantasia="Hospital Israelita,Albert Einstein",
                email_corporativo="hospitalisraelitaae@gmail.com",
                celular="(88) 7 1010-3210",
                idade=10,
                faturamento=Decimal("50000000"),
                categoria="Saúde",
                saldo=Decimal("450000000"),
            )
        ]


def test_listar_sucesso():
    controller = PessoaJuridicaListarController(MockPessoaJuridicaRepository(retornar_vazio=False))  # type: ignore

    response = controller.listar()

    expected_response = {
        "data": {
            "type": "Pessoa Jurídica",
            "count": 1,
            "attributes": [
                {
                    "nome_fantasia": "Hospital Israelita,Albert Einstein",
                    "email_corporativo": "hospitalisraelitaae@gmail.com",
                    "celular": "(88) 7 1010-3210",
                    "idade": 10,
                    "faturamento": Decimal("50000000"),
                    "categoria": "Saúde",
                    "saldo": Decimal("450000000"),
                }
            ],
        }
    }

    assert response == expected_response


def test_nao_encontrado():
    controller = PessoaJuridicaListarController(MockPessoaJuridicaRepository(retornar_vazio=True))  # type: ignore

    with pytest.raises(HttpNotFoundError) as exc_info:
        controller.listar()

    assert "Nenhuma Pessoa Jurídica Cadastrada" in str(exc_info.value)


def test_listar_multiplas_pessoas():
    class MockRepositoryMultiplo:
        def listar_todas(self):
            return [
                MockPessoaJuridica(
                    nome_fantasia="Hospital Sírio-Libanês",
                    email_corporativo="hospitalsirioliba@gmail.com",
                    celular="(88) 8 1021-1230",
                    idade=10,
                    faturamento=Decimal("39000000"),
                    categoria="Saúde",
                    saldo=Decimal("650000000"),
                ),
                MockPessoaJuridica(
                    nome_fantasia="Hospital Alemão Oswaldo Cruz",
                    email_corporativo="hospitalaleoswcru@gmail.com",
                    celular="(88) 9 1320-1201",
                    idade=10,
                    faturamento=Decimal("39000000"),
                    categoria="Saúde",
                    saldo=Decimal("650000000"),
                ),
            ]

    controller = PessoaJuridicaListarController(MockRepositoryMultiplo())  # type: ignore
    response = controller.listar()

    assert response["data"]["count"] == 2
    assert len(response["data"]["attributes"]) == 2
    assert (
        response["data"]["attributes"][0]["nome_fantasia"] == "Hospital Sírio-Libanês"
    )
    assert (
        response["data"]["attributes"][1]["nome_fantasia"]
        == "Hospital Alemão Oswaldo Cruz"
    )
