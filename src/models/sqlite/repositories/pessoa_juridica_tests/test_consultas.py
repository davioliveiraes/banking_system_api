from decimal import Decimal
from unittest.mock import Mock

from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable


class TestBuscarPorCategoria:

    def test_buscar_por_categoria_encontrada(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        lista_mocks = [
            Mock(id=1, nome_fantasia="Meta", categoria="Tecnologia"),
            Mock(id=2, nome_fantasia="Google", categoria="Tecnologia"),
            Mock(id=3, nome_fantasia="Nvidea", categoria="Tecnologia"),
        ]

        mock_session.query.return_value.filter.return_value.all.return_value = (
            lista_mocks
        )

        resultado = repository.buscar_por_categoria("Tecnologia")

        assert isinstance(resultado, list)
        assert len(resultado) == 3
        assert resultado[0].categoria == "Tecnologia"  # type: ignore
        mock_session.query.assert_called_once_with(PessoaJuridicaTable)

    def test_buscar_por_categoria_vazia(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.all.return_value = []

        resultado = repository.buscar_por_categoria("Categoria inexistente")

        assert isinstance(resultado, list)
        assert len(resultado) == 0

    def test_buscar_por_categoria_multiplas_empresas(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        lista_empresas = [
            Mock(id=1, nome_fantasia="Insider", categoria="Roupas"),
            Mock(id=2, nome_fantasia="Alpha", categoria="Roupas"),
            Mock(id=3, nome_fantasia="Eazy", categoria="Roupas"),
            Mock(id=4, nome_fantasia="Omni", categoria="Roupas"),
            Mock(id=5, nome_fantasia="Sieg", categoria="Roupas"),
        ]

        mock_session.query.return_value.filter.return_value.all.return_value = (
            lista_empresas
        )

        resultado = repository.buscar_por_categoria("Roupas")

        assert len(resultado) == 5
        assert resultado[0].categoria == "Roupas"  # type: ignore
        ids = [empresa.id for empresa in resultado]
        assert len(ids) == 5


class TestBuscarPorSaldoMaiorQue:

    def test_buscar_por_saldo_maior_que(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        lista_empresas = [
            Mock(id=1, saldo=Decimal("100000.00")),
            Mock(id=2, saldo=Decimal("500000.00")),
            Mock(id=3, saldo=Decimal("1000000.00")),
        ]

        mock_session.query.return_value.filter.return_value.all.return_value = (
            lista_empresas
        )

        valor_referente = Decimal("50000.00")
        resultado = repository.buscar_por_saldo_maior_que(valor_referente)

        assert len(resultado) == 3
        saldos = [empresa.saldo > valor_referente for empresa in resultado]
        assert all(saldos)

    def test_buscar_por_saldo_maior_que_vazio(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.all.return_value = []

        valor_referente = Decimal("999999999.00")
        resultado = repository.buscar_por_saldo_maior_que(valor_referente)

        assert resultado == []
        assert len(resultado) == 0

    def test_buscar_por_saldo_maior_que_limite_exato(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_session.query.return_value.filter.return_value.all.return_value = [
            Mock(id=2, saldo=Decimal("50000.01"))
        ]

        valor_referente = Decimal("50000.00")
        resultado = repository.buscar_por_saldo_maior_que(valor_referente)

        assert len(resultado) == 1
        assert resultado[0].saldo == Decimal("50000.01")  # type: ignore


class TestBuscarComFaturamentoMaiorQue:

    def test_buscar_com_faturamento_maior_que(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        lista_empresas = [
            Mock(id=1, faturamento=Decimal("20000000.00")),
            Mock(id=2, faturamento=Decimal("80000000.00")),
            Mock(id=3, faturamento=Decimal("50000000.00")),
            Mock(id=4, faturamento=Decimal("70000000.00")),
            Mock(id=5, faturamento=Decimal("90000000.00")),
        ]

        mock_session.query.return_value.filter.return_value.all.return_value = (
            lista_empresas
        )

        valor_referente = Decimal("250000.00")
        resultado = repository.buscar_com_faturamento_maior_que(valor_referente)

        assert len(resultado) == 5
        faturamentos = [empresa.faturamento > valor_referente for empresa in resultado]
        assert all(faturamentos)

    def test_buscar_com_faturamento_maior_que_vazio(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.all.return_value = []

        valor_referente = Decimal("999999999.00")
        resultado = repository.buscar_com_faturamento_maior_que(valor_referente)

        assert resultado == []
        assert len(resultado) == 0

    def test_com_faturamento_maior_que_exato(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_session.query.return_value.filter.return_value.all.return_value = [
            Mock(id=2, faturamento=Decimal("100000.01"))
        ]

        valor_referente = Decimal("100000.00")
        resultado = repository.buscar_com_faturamento_maior_que(valor_referente)

        assert len(resultado) == 1
        assert resultado[0].faturamento == Decimal("100000.01")  # type: ignore


class TestBuscarPorIdadeEmpresa:

    def test_buscar_por_idade_empresa_dentro_range(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_session.query.return_value.filter.return_value.all.return_value = [
            Mock(id=2, idade=10),
            Mock(id=3, idade=15),
            Mock(id=4, idade=20),
        ]

        idade_min = 10
        idade_max = 20
        resultado = repository.buscar_por_idade_empresa(idade_min, idade_max)

        assert len(resultado) == 3
        idades = [idade_min <= empresa.idade <= idade_max for empresa in resultado]
        assert all(idades)

    def test_buscar_por_idade_empresa_fora_range(self, db_session_mock, repository):
        _, mock_session = db_session_mock
        mock_session.query.return_value.filter.return_value.all.return_value = []

        resultado = repository.buscar_por_idade_empresa(100, 150)

        assert resultado == []
        assert len(resultado) == 0

    def test_buscar_por_idade_empresa_limite_min(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_session.query.return_value.filter.return_value.all.return_value = [
            Mock(id=2, idade=10),
            Mock(id=3, idade=15),
        ]

        idade_min = 10
        idade_max = 20
        resultado = repository.buscar_por_idade_empresa(idade_min, idade_max)

        assert len(resultado) == 2
        assert resultado[0].idade == 10  # type: ignore
        assert resultado[1].idade == 15  # type: ignore

    def test_buscar_por_idade_empresa_max(self, db_session_mock, repository):
        _, mock_session = db_session_mock

        mock_session.query.return_value.filter.return_value.all.return_value = [
            Mock(id=1, idade=15),
            Mock(id=2, idade=20),
        ]

        idade_min = 10
        idade_max = 20
        resultado = repository.buscar_por_idade_empresa(idade_min, idade_max)

        assert len(resultado) == 2
        assert resultado[0].idade == 15  # type: ignore
        assert resultado[1].idade == 20  # type: ignore
        idades = [empresa.idade <= idade_max for empresa in resultado]
        assert all(idades)
