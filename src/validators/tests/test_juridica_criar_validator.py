from decimal import Decimal

import pytest

from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.validators.juridica_criar_validator import juridica_criar_validator
from src.views.http_types.http_request import HttpRequest


def test_validator_sucesso():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "(22) 9 1230-1232",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    result = juridica_criar_validator(http_request)

    assert result["nome_fantasia"] == "Hospital Geral Dr. Waldemar Alcântara"
    assert result["email_corporativo"] == "hoswaldemaralcantara@gmail.com"
    assert result["celular"] == "22912301232"
    assert result["idade"] == 20
    assert result["faturamento"] == Decimal("100000.00")
    assert result["categoria"] == "Saúde"
    assert result["saldo"] == Decimal("120000.00")


def test_validator_celular_sem_formatacao():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    result = juridica_criar_validator(http_request)

    assert result["celular"] == "22912301232"


def test_validator_idade_zero():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 0,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    result = juridica_criar_validator(http_request)

    assert result["idade"] == 0


def test_validator_email_corporativo_invalido():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@invalido",
            "celular": "(22) 9 1230-1232",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "email_corporativo" in str(exc_info.value).lower()


def test_validator_idade_negativa():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": -1,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "idade" in str(exc_info.value).lower()


def test_validator_idade_maior_200():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 201,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "idade" in str(exc_info.value).lower()


def test_validator_celular_invalido_muito_curto():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "celular" in str(exc_info.value).lower()


def test_validator_celular_invalido_muito_longo():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "2291230123212",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "celular" in str(exc_info.value).lower()


def test_validator_campo_faltando():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 20,
            # Faltando o campo faturamento
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "faturamento" in str(exc_info.value).lower()


def test_validator_faturamento_negativo():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 20,
            "faturamento": -1,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "faturamento" in str(exc_info.value).lower()


def test_validator_saldo_negativo():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": -1,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "saldo" in str(exc_info.value).lower()


def test_validator_nome_fantasia_muito_curto():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "HO",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "nome_fantasia" in str(exc_info.value).lower()


def test_validator_nome_fantasia_vazio():
    http_request = HttpRequest(
        body={
            "nome_fantasia": " ",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": "Saúde",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "nome_fantasia" in str(exc_info.value).lower()


def test_validator_categoria_vazia():
    http_request = HttpRequest(
        body={
            "nome_fantasia": "Hospital Geral Dr. Waldemar Alcântara",
            "email_corporativo": "hoswaldemaralcantara@gmail.com",
            "celular": "22912301232",
            "idade": 20,
            "faturamento": 100000.00,
            "categoria": " ",
            "saldo": 120000.00,
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        juridica_criar_validator(http_request)

    assert "categoria" in str(exc_info.value).lower()
