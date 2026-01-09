from decimal import Decimal
from unittest.mock import Mock

from sqlalchemy.exc import NoResultFound

from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable


class TestCriarEmpresa:

    def test_criar_empresa_sucesso(self, db_session_mock, repository, empresa_data):
        _, mock_session = db_session_mock
        mock_session.refresh = Mock(side_effect=lambda obj: setattr(obj, "id", 1))

        resultado = repository.criar_empresa(empresa_data)

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert resultado is not None


class TestBuscarPorId:

    def test_buscar_por_id_encontrada(
        self, db_session_mock, repository, mock_empresa_padrao
    ):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa_padrao
        )

        resultado = repository.buscar_por_id(1)

        assert resultado is not None
        assert resultado.id == 1  # type: ignore
        assert resultado.nome_fantasia == "Pearson Specter Litt"  # type: ignore
        mock_session.query.assert_called_once_with(PessoaJuridicaTable)

    def test_buscar_por_id_nao_encontrado(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.buscar_por_id(999)

        assert resultado is None


class TestBuscarPorEmailCorporativo:

    def test_buscar_por_email_corporativo_encontrado(
        self, db_session_mock, repository, mock_empresa_padrao
    ):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa_padrao
        )

        resultado = repository.buscar_por_email_corporativo(
            "pearson_specter_litt@gmail.com"
        )

        assert resultado is not None
        assert (
            resultado.email_corporativo  # type: ignore
            == "pearson_specter_litt@gmail.com"
        )

    def test_buscar_por_email_corporativo_nao_encontrado(
        self, db_session_mock, repository
    ):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.buscar_por_email_corporativo("naoexiste@gmail.com")

        assert resultado is None


class TestBuscarPorCelular:

    def test_buscar_por_celular_encontrado(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.celular = "555-9001"

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        resultado = repository.buscar_por_celular("555-9001")

        assert resultado is not None
        assert resultado.celular == "555-9001"  # type: ignore

    def test_buscar_por_celular_nao_encontrado(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.buscar_por_celular("1234-1231")

        assert resultado is None


class TestListarTodas:

    def test_listar_todas(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa_1 = Mock()
        mock_empresa_1.id = 1
        mock_empresa_1.nome_fantasia = "Pearson Specter Litt"

        mock_empresa_2 = Mock()
        mock_empresa_2.id = 2
        mock_empresa_2.nome_fantasia = "Zane Specter Litt"

        mock_session.query.return_value.all.return_value = [
            mock_empresa_1,
            mock_empresa_2,
        ]

        resultado = repository.listar_todas()

        assert len(resultado) == 2
        assert resultado[0].nome_fantasia == "Pearson Specter Litt"  # type: ignore
        assert resultado[1].nome_fantasia == "Zane Specter Litt"  # type: ignore


class TestAtualizarEmpresa:

    def test_atualizar_empresa_sucesso(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.nome_fantasia = "Darby International"
        mock_empresa.email_corporativo = "contato@darbyintl.com"
        mock_empresa.celular = "555-2005"

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        dados_atualizacao = {
            "email_corporativo": "contato@darbyintnew.com",
            "celular": "554-7777",
        }

        resultado = repository.atualizar_empresa(1, dados_atualizacao)

        assert resultado is not None
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_atualizar_empresa_nao_encontrada(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.one.side_effect = (
            NoResultFound()
        )

        resultado = repository.atualizar_empresa(
            999, {"email_corporativo": "contato@darbyintlinexistente.com"}
        )

        assert resultado is None

    def test_atualizar_empresa_campo_nao_permitidos(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_empresa = Mock()
        mock_empresa.id = 1
        mock_empresa.saldo = Decimal("500000.00")

        mock_session.query.return_value.filter.return_value.one.return_value = (
            mock_empresa
        )

        dados_atualizacao = {
            "id": 999,
            "saldo": Decimal("50000.00"),
            "nome_fantasia": "Nome empresa nova",
        }

        resultado = repository.atualizar_empresa(1, dados_atualizacao)

        assert resultado is not None
        assert mock_empresa.id == 1
        assert mock_empresa.saldo == Decimal("500000.00")


class TestDeletarEmpresa:

    def test_deletar_empresa_sucesso(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.delete.return_value = 1

        resultado = repository.deletar_empresa(1)

        assert resultado is True
        mock_session.commit.assert_called_once()

    def test_deletar_empresa_nao_encontrada(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.delete.return_value = 0

        resultado = repository.deletar_empresa(999)

        assert resultado is False
