from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import NoResultFound


class TestSacarDinheiro:

    def test_sacar_dinheiro_sucesso(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("200000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.sacar_dinheiro(1, Decimal("10000.00"))

        assert resultado is True
        assert mock_empresa.saldo == Decimal("190000.00")
        mock_session.commit.assert_called_once()

    def test_sacar_dinheiro_saldo_insuficiente(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("1000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        with pytest.raises(ValueError, match="Saldo Insuficiente"):
            repository.sacar_dinheiro(1, Decimal("3000.00"))

    def test_sacar_dinheiro_valor_negativo(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("50000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        with pytest.raises(ValueError, match="Valor de saque deve ser positivo"):
            repository.sacar_dinheiro(1, Decimal("-1000.00"))

    def test_sacar_valor_zero(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("50000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        with pytest.raises(ValueError, match="Valor de saque deve ser positivo"):
            repository.sacar_dinheiro(1, Decimal("0.00"))

    def test_sacar_valor_exato(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("50000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.sacar_dinheiro(1, Decimal("50000.00"))

        assert resultado is True
        assert mock_empresa.saldo == Decimal("0.00")
        mock_session.commit.assert_called_once()

    def test_sacar_com_centavos(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("1500.55")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.sacar_dinheiro(1, Decimal("500.50"))

        assert resultado is True
        assert mock_empresa.saldo == Decimal("1000.05")
        mock_session.commit.assert_called_once()

    def test_sacar_empresa_nao_encontrada(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Empresa com ID 999 não encontrada"):
            repository.sacar_dinheiro(999, Decimal("100000.00"))


class TestDepositarDinheiro:

    def test_depositar_dinheiro_sucesso(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("10000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.depositar_dinheiro(1, Decimal("5000.00"))

        assert resultado is True
        assert mock_empresa.saldo == Decimal("15000.00")
        mock_session.commit.assert_called_once()

    def test_depositar_valor_negativo(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("10000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        with pytest.raises(ValueError, match="Valor de depósito deve ser positivo"):
            repository.depositar_dinheiro(1, Decimal("-1000.00"))

    def test_depositar_valor_zero(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("10000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        with pytest.raises(ValueError, match="Valor de depósito deve ser positivo"):
            repository.depositar_dinheiro(1, Decimal("0.00"))

    def test_depositar_com_centavos(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("10500.50")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.depositar_dinheiro(1, Decimal("500.25"))

        assert resultado is True
        assert mock_empresa.saldo == Decimal("11000.75")
        mock_session.commit.assert_called_once()

    def test_depositar_valor_grande(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("4000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.depositar_dinheiro(1, Decimal("1500000000.00"))

        assert resultado is True
        assert mock_empresa.saldo == Decimal("1500004000.00")
        mock_session.commit.assert_called_once()

    def test_depositar_empresa_nao_encontrada(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Empresa com ID 999 não encontrada"):
            repository.depositar_dinheiro(999, Decimal("10000.00"))


class TestObterSaldo:

    def test_obter_saldo_sucesso(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_resultado = Mock()
        mock_resultado.saldo = Decimal("90000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_resultado
        )

        resultado = repository.obter_saldo(1)

        assert resultado == Decimal("90000.00")
        assert isinstance(resultado, Decimal)

    def test_obter_saldo_empresa_nao_encontrada(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Empresa com ID 999 não encontrada"):
            repository.obter_saldo(999)


class TestRealizarExtrato:

    def test_realizar_extrato_sucesso(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.nome_fantasia = "Rand Corporation"
        mock_empresa.email_corporativo = "contato@randcorp.com"
        mock_empresa.saldo = float(150000.00)
        mock_empresa.categoria = "Cliente Corporativo"
        mock_empresa.idade = 8
        mock_empresa.criado_em = datetime(2025, 11, 30, 10, 0, 0)
        mock_empresa.atualizado_em = datetime(2026, 1, 1, 13, 30, 0)

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.realizar_extrato(1)

        assert resultado["id"] == 1
        assert resultado["nome_fantasia"] == "Rand Corporation"
        assert resultado["email_corporativo"] == "contato@randcorp.com"
        assert resultado["saldo"] == float(150000.00)
        assert resultado["categoria"] == "Cliente Corporativo"
        assert resultado["idade"] == 8
        assert "criado_em" in resultado
        assert "atualizado_em" in resultado

    def test_realizar_extrato_empresa_nao_encontrada(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        with pytest.raises(ValueError, match="Empresa com ID 999 não encontrada"):
            repository.realizar_extrato(999)

    def test_realizar_extrato_formato_correto(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 2
        mock_empresa.nome_fantasia = "Pearson Specter"
        mock_empresa.email_corporativo = "contato@pearsonspecter.com"
        mock_empresa.saldo = float(200000.00)
        mock_empresa.categoria = "Escritório de Advocacia"
        mock_empresa.idade = 18
        mock_empresa.criado_em = datetime(2025, 12, 9, 15, 3, 24)
        mock_empresa.atualizado_em = datetime(2026, 1, 1, 15, 0, 30)

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.realizar_extrato(2)

        assert isinstance(resultado, dict)
        assert set(resultado.keys()) == {
            "id",
            "nome_fantasia",
            "email_corporativo",
            "saldo",
            "categoria",
            "idade",
            "criado_em",
            "atualizado_em",
        }
        assert resultado["id"] == 2
        assert resultado["nome_fantasia"] == "Pearson Specter"
        assert resultado["email_corporativo"] == "contato@pearsonspecter.com"
        assert resultado["saldo"] == float(200000.00)
        assert resultado["categoria"] == "Escritório de Advocacia"
        assert resultado["idade"] == 18
