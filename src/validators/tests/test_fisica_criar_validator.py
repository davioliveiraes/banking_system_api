from decimal import Decimal

import pytest

from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.validators.fisica_criar_validator import fisica_criar_validator
from src.views.http_types.http_request import HttpRequest


def test_validator_sucesso():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@gmail.com",
            "celular": "(32) 9 0319-1239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    result = fisica_criar_validator(http_request)

    assert result["nome_completo"] == "Dr. Shaun Murphy"
    assert result["email"] == "shaun@gmail.com"
    assert result["celular"] == "32903191239"
    assert result["idade"] == 25
    assert result["renda_mensal"] == Decimal("10000.00")
    assert result["categoria"] == "Saúde"
    assert result["saldo"] == Decimal("50000.00")


def test_validator_celular_sem_formatacao():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@gmail.com",
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    result = fisica_criar_validator(http_request)
    assert result["celular"] == "32903191239"


def test_validator_email_invalido():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@invalid",
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "email" in str(exc_info.value).lower()


def test_validator_idade_menor_18():
    http_request = HttpRequest(
        body={
            "nome_completo": "Jovem Pessoa",
            "email": "jovem@gmail.com",
            "celular": "32903191239",
            "idade": 17,
            "renda_mensal": "10000.00",
            "categoria": "Estudante",
            "saldo": "5000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    error_msg = str(exc_info.value).lower()
    assert "idade" in error_msg


def test_validator_idade_maior_120():
    http_request = HttpRequest(
        body={
            "nome_completo": "Pessoa Antiga",
            "email": "antiga@gmail.com",
            "celular": "32903191239",
            "idade": 121,
            "renda_mensal": "10000.00",
            "categoria": "Aposentado",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "idade" in str(exc_info.value).lower()


def test_validator_celular_invalido_muito_curto():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@gmail.com",
            "celular": "123",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "celular" in str(exc_info.value).lower()


def test_validator_celular_invalido_muito_longo():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@gmail.com",
            "celular": "123456789012345",  # 15 dígitos
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "celular" in str(exc_info.value).lower()


def test_validator_campo_faltando():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            # "email" faltando
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "email" in str(exc_info.value).lower()


def test_validator_saldo_negativo():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@gmail.com",
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "-1000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "saldo" in str(exc_info.value).lower()


def test_validator_renda_negativa():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@gmail.com",
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "-5000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "renda_mensal" in str(exc_info.value).lower()


def test_validator_nome_muito_curto():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr",
            "email": "shaun@gmail.com",
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "nome_completo" in str(exc_info.value).lower()


def test_validator_nome_vazio():
    http_request = HttpRequest(
        body={
            "nome_completo": "   ",
            "email": "shaun@gmail.com",
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "Saúde",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "nome_completo" in str(exc_info.value).lower()


def test_validator_categoria_vazia():
    http_request = HttpRequest(
        body={
            "nome_completo": "Dr. Shaun Murphy",
            "email": "shaun@gmail.com",
            "celular": "32903191239",
            "idade": 25,
            "renda_mensal": "10000.00",
            "categoria": "   ",
            "saldo": "50000.00",
        }
    )

    with pytest.raises(HttpBadRequestError) as exc_info:
        fisica_criar_validator(http_request)

    assert "categoria" in str(exc_info.value).lower()
