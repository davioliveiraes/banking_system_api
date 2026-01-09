from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import NoResultFound

from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.repositories.pessoa_fisica_repository import (
    PessoaFisicaRepository,
)


class TestPessoaFisicaRepository:

    # TESTE CRUD
    def test_criar_pessoa_sucesso(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        pessoa_data = {
            "nome_completo": "Harvey Specter",
            "email": "harvey@gmail.com",
            "celular": "555-1001",
            "idade": 38,
            "renda_mensal": Decimal("85000.00"),
            "categoria": "Socio Senior",
            "saldo": Decimal("2500000.00"),
        }

        mock_pessoa = PessoaFisicaTable(**pessoa_data)
        mock_pessoa.id = 1  # type: ignore
        mock_session.refresh = Mock(side_effect=lambda obj: setattr(obj, "id", 1))

        resultado = repository.criar_pessoa(pessoa_data)

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert resultado is not None

    def test_buscar_por_id_encontrado(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.nome_completo = "Harvey Specter"
        mock_pessoa.email = "harvey@example.com"

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        resultado = repository.buscar_por_id(1)

        assert resultado is not None
        assert resultado.id == 1  # type: ignore
        assert resultado.nome_completo == "Harvey Specter"  # type: ignore
        mock_session.query.assert_called_once_with(PessoaFisicaTable)

    def test_buscar_por_id_nao_encontrado(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.buscar_por_id(999)

        assert resultado is None

    def test_buscar_por_email_encontrado(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.email = "harvey@example.com"

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        resultado = repository.buscar_por_email("harvey@example.com")

        assert resultado is not None
        assert resultado.email == "harvey@example.com"  # type: ignore

    def test_buscar_por_email_nao_encontrado(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.buscar_por_email("naoexiste@example.com")

        assert resultado is None

    def test_buscar_por_celular_encontrado(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.celular = "555-1001"

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        resultado = repository.buscar_por_celular("555-1001")

        assert resultado is not None
        assert resultado.celular == "555-1001"  # type: ignore

    def test_buscar_por_celular_nao_encontrado(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.buscar_por_celular("3123-3123")

        assert resultado is None

    def test_listar_todas(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa_1 = Mock()
        mock_pessoa_1.id = 1
        mock_pessoa_1.nome_completo = "Harvey Specter"

        mock_pessoa_2 = Mock()
        mock_pessoa_2.id = 2
        mock_pessoa_2.nome_completo = "Mike Ross"

        mock_session.query.return_value.all.return_value = [
            mock_pessoa_1,
            mock_pessoa_2,
        ]

        resultado = repository.listar_todas()

        assert len(resultado) == 2
        assert resultado[0].nome_completo == "Harvey Specter"  # type: ignore
        assert resultado[1].nome_completo == "Mike Ross"  # type: ignore

    def test_atualizar_pessoa_sucesso(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.nome_completo = "Harvey Specter"
        mock_pessoa.email = "harvey@old.com"
        mock_pessoa.celular = "555-1001"

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        dados_atualizacao = {"email": "harvey_specter@new.com", "celular": "555-9999"}

        resultado = repository.atualizar_pessoa(1, dados_atualizacao)

        assert resultado is not None
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_atualizar_pessoa_nao_encontrada(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.atualizar_pessoa(
            999, {"email": "harvey@gmailinexistente.com"}
        )

        assert resultado is None

    def test_atualizar_pessoa_campos_nao_permitidos(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        dados_atualizacao = {
            "id": 999,
            "saldo": Decimal("9999.99"),
            "nome_completo": "Nome novo",
        }

        resultado = repository.atualizar_pessoa(1, dados_atualizacao)

        assert resultado is not None
        assert mock_pessoa.id == 1
        assert mock_pessoa.saldo == Decimal("1000.00")

    def test_deletar_pessoa_sucesso(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.delete.return_value = 1

        resultado = repository.deletar_pessoa(1)

        assert resultado is True
        mock_session.commit.assert_called_once()

    def test_deletar_pessoa_nao_encontrada(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.delete.return_value = 0

        resultado = repository.deletar_pessoa(999)

        assert resultado is False

    # TESTE OPERAÇÕES BANCÁRIAS

    def test_sacar_dinheiro_sucesso(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        resultado = repository.sacar_dinheiro(1, Decimal("500.00"))

        assert resultado is True
        assert mock_pessoa.saldo == Decimal("500.00")
        mock_session.commit.assert_called_once()

    def test_sacar_deposito_saldo_insuficiente(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("500.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        with pytest.raises(ValueError, match="Saldo Insuficiente"):
            repository.sacar_dinheiro(1, Decimal("1000.00"))

    def test_sacar_valor_negativo(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        with pytest.raises(ValueError, match="Valor de saque deve ser positivo"):
            repository.sacar_dinheiro(1, Decimal("-100.00"))

    def test_sacar_valor_zero(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        with pytest.raises(ValueError, match="Valor de saque deve ser positivo"):
            repository.sacar_dinheiro(1, Decimal("0.00"))

    def test_sacar_pessoa_nao_encontrada(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Pessoa com ID 999 não encontrada"):
            repository.sacar_dinheiro(999, Decimal("1000.00"))

    def test_depositar_dinheiro_sucesso(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        resultado = repository.depositar_dinheiro(1, Decimal("500.00"))

        assert resultado is True
        assert mock_pessoa.saldo == Decimal("1500.00")
        mock_session.commit.assert_called_once()

    def test_depositar_valor_negativo(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        with pytest.raises(ValueError, match="Valor de depósito deve ser positivo."):
            repository.depositar_dinheiro(1, Decimal("-500.00"))

    def test_depositar_valor_zero(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        with pytest.raises(ValueError, match="Valor de depósito deve ser positivo."):
            repository.depositar_dinheiro(1, Decimal("0.00"))

    def test_depositar_pessoa_nao_encontrada(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Pessoa com ID 999 não foi encontrada"):
            repository.depositar_dinheiro(999, Decimal("1000.00"))

    def test_obter_saldo_sucesso(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_resultado = Mock()
        mock_resultado.saldo = Decimal("50000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_resultado
        )

        resultado = repository.obter_saldo(1)

        assert resultado == Decimal("50000.00")

    def test_obter_saldo_pessoa_nao_encontrada(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Pessoa com ID 999 não encontrada"):
            repository.obter_saldo(999)

    def test_realizar_extrato_sucesso(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.id = 1
        mock_pessoa.nome_completo = "Harvey Specter"
        mock_pessoa.email = "harvey_specter@gmail.com"
        mock_pessoa.saldo = float("50000.00")
        mock_pessoa.categoria = "Socio Senior"
        mock_pessoa.criado_em = datetime(2025, 1, 1, 10, 0, 0)
        mock_pessoa.atualizado_em = datetime(2025, 1, 15, 14, 30, 0)

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_pessoa
        )

        resultado = repository.realizar_extrato(1)

        assert resultado["id"] == 1
        assert resultado["nome_completo"] == "Harvey Specter"
        assert resultado["email"] == "harvey_specter@gmail.com"
        assert resultado["saldo"] == float("50000.00")
        assert resultado["categoria"] == "Socio Senior"
        assert "criado_em" in resultado
        assert "atualizado_em" in resultado

    def test_realizar_extrato_pessoa_nao_encontrada(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Pessoa com ID 999 não encontrada"):
            repository.realizar_extrato(999)

    # TESTE (Consultas Específicas)

    def test_buscar_por_categoria(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.categoria = "Socio Senior"

        mock_session.query.return_value.filter.return_value.all.return_value = [
            mock_pessoa
        ]

        resultado = repository.buscar_por_categoria("Socio Senior")

        assert resultado is not None
        assert len(resultado) == 1
        assert resultado[0].categoria == "Socio Senior"  # type: ignore
        mock_session.query.assert_called_once_with(PessoaFisicaTable)

    def test_buscar_com_saldo_maior_que(self):
        mock_db_connection = Mock()
        mock_session = Mock()
        mock_db_connection.__enter__ = Mock(return_value=mock_db_connection)
        mock_db_connection.__exit__ = Mock(return_value=False)
        mock_db_connection.session = mock_session

        repository = PessoaFisicaRepository(mock_db_connection)

        mock_pessoa = Mock()
        mock_pessoa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.all.return_value = [
            mock_pessoa
        ]

        resultado = repository.buscar_com_saldo_maior_que(Decimal("500.00"))

        assert resultado is not None
        assert len(resultado) == 1
        assert resultado[0].saldo == Decimal("1000.00")  # type: ignore
        mock_session.query.assert_called_once_with(PessoaFisicaTable)
