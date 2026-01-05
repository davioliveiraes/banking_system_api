from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from src.models.sqlite.repositories.pessoa_juridica_repository import (
    PessoaJuridicaRepository,
)


@pytest.fixture
def db_session_mock():
    """Fixture que configura mock do db_connection e session."""
    mock_db_connection = Mock()
    mock_session = Mock()
    mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
    mock_db_connection.__exit__ = Mock(return_value=False)
    mock_db_connection.session = mock_session
    return mock_db_connection, mock_session


@pytest.fixture
def repository(db_session_mock):
    """Fixture que retorna o repositório com conexão mockada."""
    mock_db_connection, _ = db_session_mock
    return PessoaJuridicaRepository(mock_db_connection)


@pytest.fixture
def mock_empresa_padrao():
    """Fixture que retorna uma empresa mock padrão."""
    mock_empresa = Mock()
    mock_empresa.id = 1
    mock_empresa.nome_fantasia = "Pearson Specter Litt"
    mock_empresa.email_corporativo = "pearson_specter_litt@gmail.com"
    mock_empresa.celular = "555-2001"
    mock_empresa.idade = 10
    mock_empresa.faturamento = Decimal("40000000.00")
    mock_empresa.categoria = "Escritório de Advocacia"
    mock_empresa.saldo = Decimal("95000000.00")
    mock_empresa.criado_em = datetime(2025, 11, 30, 10, 0, 0)
    mock_empresa.atualizado_em = datetime(2026, 1, 1, 13, 30, 0)
    return mock_empresa


@pytest.fixture
def empresa_data():
    """Fixture que retorna dados para criação de empresa."""
    return {
        "nome_fantasia": "Pearson Specter Litt",
        "email_corporativo": "pearson_specter_litt@gmail.com",
        "celular": "555-2001",
        "idade": 10,
        "faturamento": Decimal("40000000.00"),
        "categoria": "Escritório de Advocacia",
        "saldo": Decimal("95000000.00"),
    }
