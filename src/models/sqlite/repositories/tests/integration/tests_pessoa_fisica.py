from decimal import Decimal

import pytest

from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.repositories.pessoa_fisica_repository import (
    PessoaFisicaRepository,
)
from src.models.sqlite.settings.connection import db_connection_handler

db_connection_handler.connect_to_be()


# PESSOA FISÍCA
# CRUD
@pytest.mark.skip(reason="integracao com banco de dados")
def test_criar_pessoa():
    pessoa_data = {
        "renda_mensal": Decimal("8000.00"),
        "idade": 30,
        "nome_completo": "Naruto Usumaki",
        "celular": "555-456",
        "email": "narutousumaki@gmail.com",
        "categoria": "Hokage",
        "saldo": Decimal("500.00"),
    }

    repository = PessoaFisicaRepository(db_connection_handler)
    pessoa_criada = repository.criar_pessoa(pessoa_data)

    assert pessoa_criada is not None
    assert pessoa_criada.id is not None
    assert pessoa_criada.nome_completo == "Naruto Usumaki"  # type: ignore
    assert pessoa_criada.saldo == Decimal("500.00")  # type: ignore
    assert pessoa_criada.email == "narutousumaki@gmail.com"  # type: ignore
    assert pessoa_criada.renda_mensal == Decimal("8000.00")  # type: ignore
    assert pessoa_criada.idade == 30  # type: ignore
    assert pessoa_criada.categoria == "Hokage"  # type: ignore
    assert pessoa_criada.celular == "555-456"  # type: ignore


@pytest.mark.skip(reason="integracao com banco de dados")
def test_buscar_por_id():
    repository = PessoaFisicaRepository(db_connection_handler)
    pessoa = repository.buscar_por_id(1)

    print(f"\nID: {pessoa.id}; Nome Completo: {pessoa.nome_completo} ")  # type: ignore

    assert pessoa is not None
    assert pessoa.id == 1  # type: ignore
    assert isinstance(pessoa, PessoaFisicaTable)


@pytest.mark.skip(reason="integracao com banco de dados")
def test_buscar_por_email():
    repository = PessoaFisicaRepository(db_connection_handler)
    pessoa = repository.buscar_por_email("gaaradodeserto@gmail.com")

    print(f"\nEmail: {pessoa.email}; Nome Completo: {pessoa.nome_completo}")  # type: ignore

    assert pessoa is not None
    assert pessoa.id is not None
    assert pessoa.email == "gaaradodeserto@gmail.com"  # type: ignore
    assert isinstance(pessoa, PessoaFisicaTable)


@pytest.mark.skip(reason="integracao com banco de dados")
def test_buscar_por_celular():
    repository = PessoaFisicaRepository(db_connection_handler)
    pessoa = repository.buscar_por_celular("987-1001")

    print(f"\nCelular: {pessoa.celular}; Nome Completo: {pessoa.nome_completo}")  # type: ignore

    assert pessoa is not None
    assert pessoa.id is not None
    assert pessoa.celular == "987-1001"  # type: ignore
    assert isinstance(pessoa, PessoaFisicaTable)


@pytest.mark.skip(reason="integracao com banco de dados")
def test_listar_todas():
    repository = PessoaFisicaRepository(db_connection_handler)
    lista_pessoas = repository.listar_todas()

    print(f"\nLista de pessoas: {lista_pessoas}")

    assert lista_pessoas is not None
    assert len(lista_pessoas) > 0
    assert isinstance(lista_pessoas, list)
    assert all(isinstance(p, PessoaFisicaTable) for p in lista_pessoas)


@pytest.mark.skip(reason="integracao com banco de dados")
def test_atualizar_pessoa():
    dados_atualizacao = {
        "nome_completo": "Gaara do Deserto",
        "email": "gaaradodeserto@gmail.com",
        "celular": "987-1001",
        "categoria": "Kazekage",
        "renda_mensal": Decimal("90000.00"),
        "idade": 29,
    }

    repository = PessoaFisicaRepository(db_connection_handler)
    dados_atualizados = repository.atualizar_pessoa(3, dados_atualizacao)

    assert dados_atualizados is not None
    assert dados_atualizados.id is not None
    assert dados_atualizados.id == 3  # type: ignore
    assert dados_atualizados.nome_completo == "Gaara do Deserto"  # type: ignore
    assert dados_atualizados.renda_mensal == Decimal("90000.00")  # type: ignore
    assert dados_atualizados.email == "gaaradodeserto@gmail.com"  # type: ignore
    assert dados_atualizados.categoria == "Kazekage"  # type: ignore
    assert dados_atualizados.idade == 29  # type: ignore


@pytest.mark.skip(reason="integracao com banco de dados")
def test_deletar_pessoa():
    repository = PessoaFisicaRepository(db_connection_handler)
    deletar_pessoa = repository.deletar_pessoa(4)

    assert deletar_pessoa is True
    pessoa_deletada = repository.buscar_por_id(4)
    assert pessoa_deletada is None


# OPERAÇÕES BANCÁRIAS
@pytest.mark.skip(reason="integracao com banco de dados")
def test_sacar_dinheiro():
    repository = PessoaFisicaRepository(db_connection_handler)

    saldo_anterior = repository.obter_saldo(1)
    print(f"\nSaldo anterior: {saldo_anterior}")
    print("Sacando...500000.00")

    sacando = repository.sacar_dinheiro(1, Decimal("500000.00"))
    saldo_atual = repository.obter_saldo(1)

    print(f"\nSaldo atual: {saldo_atual}")

    assert sacando is True
    assert isinstance(saldo_atual, Decimal)
    assert saldo_atual == saldo_anterior - Decimal("500000.00")
    assert saldo_atual < saldo_anterior


@pytest.mark.skip(reason="integracao com banco de dados")
def test_depositar_dinheiro():
    repository = PessoaFisicaRepository(db_connection_handler)

    saldo_anterior = repository.obter_saldo(1)
    print(f"\nSaldo Anterior: {saldo_anterior}")
    print("Depositando...500000.00")

    depositando = repository.depositar_dinheiro(1, Decimal("500000.00"))
    saldo_atual = repository.obter_saldo(1)

    print(f"\nSaldo atual: {saldo_atual}")

    assert depositando is True
    assert isinstance(saldo_atual, Decimal)
    assert saldo_atual == saldo_anterior + Decimal("500000.00")
    assert saldo_atual > saldo_anterior


@pytest.mark.skip(reason="integracao com banco de dados")
def test_obter_saldo():
    repository = PessoaFisicaRepository(db_connection_handler)
    saldo_atual = repository.obter_saldo(1)

    print(f"\n Saldo atual: {saldo_atual}")

    assert saldo_atual is not None
    assert isinstance(saldo_atual, Decimal)
    assert saldo_atual >= 0


@pytest.mark.skip(reason="integracao com banco de dados")
def test_realizar_extrato():
    repository = PessoaFisicaRepository(db_connection_handler)
    extrato = repository.realizar_extrato(8)

    print(f"\nExtrato: {extrato}")

    assert extrato is not None
    assert isinstance(extrato, dict)
    assert "id" in extrato
    assert "nome_completo" in extrato
    assert "email" in extrato
    assert "saldo" in extrato
    assert "categoria" in extrato
    assert "criado_em" in extrato
    assert "atualizado_em" in extrato
    assert extrato["id"] == 8
    assert isinstance(extrato["saldo"], float)
    assert extrato["saldo"] >= 0


@pytest.mark.skip(reason="integracao com banco de dados")
def test_sacar_dinheiro_saldo_insuficiente():
    repository = PessoaFisicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Saldo Insuficiente"):
        repository.sacar_dinheiro(1, Decimal("99999999999.99"))


@pytest.mark.skip(reason="integracao com banco de dados")
def test_sacar_dinheiro_valor_zero():
    repository = PessoaFisicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Valor de saque deve ser positivo"):
        repository.sacar_dinheiro(1, Decimal("0.00"))


@pytest.mark.skip(reason="integracao com banco de dados")
def test_depositar_dinheiro_valor_negativo():
    repository = PessoaFisicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Valor de depósito deve ser positivo"):
        repository.depositar_dinheiro(1, Decimal("-100.00"))


@pytest.mark.skip(reason="integracao com banco de dados")
def test_obter_saldo_pessoa_inexistente():
    repository = PessoaFisicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Pessoa com ID 999 não encontrada"):
        repository.obter_saldo(999)


# CONSULTAS ESPECÍFICAS
@pytest.mark.skip(reason="integracao com banco de dados")
def test_buscar_por_categoria():
    repository = PessoaFisicaRepository(db_connection_handler)
    categoria = repository.buscar_por_categoria("Socio Senior")

    print(f"Pessoas Encontradas: {categoria}")

    assert categoria is not None
    assert isinstance(categoria, list)
    assert len(categoria) > 0
    assert all(isinstance(p, PessoaFisicaTable) for p in categoria)
    assert all(p.categoria == "Socio Senior" for p in categoria)


@pytest.mark.skip(reason="integracao com banco de dados")
def test_buscar_com_saldo_maior_que():
    repository = PessoaFisicaRepository(db_connection_handler)

    valor_minimo = Decimal("1000000.00")
    buscar_saldo_maior = repository.buscar_com_saldo_maior_que(valor_minimo)

    print(f"Lista de saldos: {buscar_saldo_maior}")

    assert buscar_saldo_maior is not None
    assert isinstance(buscar_saldo_maior, list)
    if len(buscar_saldo_maior) > 0:
        assert all(isinstance(p, PessoaFisicaTable) for p in buscar_saldo_maior)
        assert all(p.saldo > valor_minimo for p in buscar_saldo_maior)
