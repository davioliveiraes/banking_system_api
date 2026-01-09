from decimal import Decimal

import pytest

from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.repositories.pessoa_juridica_repository import (
    PessoaJuridicaRepository,
)
from src.models.sqlite.settings.connection import db_connection_handler

db_connection_handler.connect_to_be()


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_criar_empresa():
    empresa_data = {
        "faturamento": Decimal("2500000.00"),
        "idade": 15,
        "nome_fantasia": "Drop Shop Brasil",
        "celular": "888-1001",
        "email_corporativo": "comercial@dropshop.com.br",
        "categoria": "premium",
        "saldo": Decimal("150000.00"),
    }

    repository = PessoaJuridicaRepository(db_connection_handler)
    empresa_criada = repository.criar_empresa(empresa_data)

    assert empresa_criada is not None
    assert empresa_criada.id is not None
    assert empresa_criada.nome_fantasia == "Drop Shop Brasil"  # type: ignore
    assert empresa_criada.saldo == Decimal("150000.00")  # type: ignore
    assert empresa_criada.email_corporativo == "comercial@dropshop.com.br"  # type: ignore
    assert empresa_criada.faturamento == Decimal("2500000.00")  # type: ignore
    assert empresa_criada.idade == 15  # type: ignore
    assert empresa_criada.categoria == "premium"  # type: ignore
    assert empresa_criada.celular == "888-1001"  # type: ignore


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_buscar_por_id():
    repository = PessoaJuridicaRepository(db_connection_handler)
    empresa = repository.buscar_por_id(7)

    print(f"\nID: {empresa.id}; Nome Fantasia: {empresa.nome_fantasia}")  # type: ignore

    assert empresa is not None
    assert empresa.id == 7  # type: ignore
    assert isinstance(empresa, PessoaJuridicaTable)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_buscar_por_email_corporativo():
    repository = PessoaJuridicaRepository(db_connection_handler)
    empresa = repository.buscar_por_email_corporativo("comercial@dropshop.com.br")

    print(f"\nEmail Corporativo: {empresa.email_corporativo}; Nome Fantasia: {empresa.nome_fantasia}")  # type: ignore

    assert empresa is not None
    assert empresa.id is not None
    assert empresa.email_corporativo == "comercial@dropshop.com.br"  # type: ignore
    assert isinstance(empresa, PessoaJuridicaTable)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_buscar_por_celular():
    repository = PessoaJuridicaRepository(db_connection_handler)
    empresa = repository.buscar_por_celular("888-1001")

    print(f"\nCelular: {empresa.celular}; Nome Fantasia: {empresa.nome_fantasia}")  # type: ignore

    assert empresa is not None
    assert empresa.id is not None
    assert empresa.celular == "888-1001"  # type: ignore
    assert isinstance(empresa, PessoaJuridicaTable)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_listar_todos():
    repository = PessoaJuridicaRepository(db_connection_handler)
    lista_empresas = repository.listar_todas()

    print(f"\n Lista de empresas: {lista_empresas}")

    assert lista_empresas is not None
    assert len(lista_empresas) > 0
    assert isinstance(lista_empresas, list)
    assert all(isinstance(p, PessoaJuridicaTable) for p in lista_empresas)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_atualiza_empresa():
    dados_atualizacao = {
        "nome_fantasia": "Shark Beach Tennis",
        "email_corporativo": "vendas@sharkbt.com.br",
        "celular": "888-0989",
        "categoria": "premium",
        "faturamento": Decimal("5800000.00"),
        "idade": 12,
    }

    repository = PessoaJuridicaRepository(db_connection_handler)
    empresa_dados_atualizados = repository.atualizar_empresa(6, dados_atualizacao)

    assert empresa_dados_atualizados is not None
    assert empresa_dados_atualizados.id is not None
    assert empresa_dados_atualizados.id == 6  # type: ignore
    assert empresa_dados_atualizados.nome_fantasia == "Shark Beach Tennis"  # type: ignore
    assert empresa_dados_atualizados.email_corporativo == "vendas@sharkbt.com.br"  # type: ignore
    assert empresa_dados_atualizados.celular == "888-0989"  # type: ignore
    assert empresa_dados_atualizados.categoria == "premium"  # type: ignore
    assert empresa_dados_atualizados.faturamento == Decimal("5800000.00")  # type: ignore
    assert empresa_dados_atualizados.idade == 12  # type: ignore


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_deletar_empresa():
    repository = PessoaJuridicaRepository(db_connection_handler)
    deletar_empresa = repository.deletar_empresa(5)

    assert deletar_empresa is True
    pessoa_deletada = repository.buscar_por_id(5)
    assert pessoa_deletada is None


# OPERAÇÕES BANCÁRIAS
@pytest.mark.skip(reason="integracao com o banco de dados")
def test_sacar_dinheiro():
    repository = PessoaJuridicaRepository(db_connection_handler)

    saldo_anterior = repository.obter_saldo(1)
    print(f"\n Saldo anterior: {saldo_anterior}")
    print("Sacando...20000000.00")

    sacando = repository.sacar_dinheiro(1, Decimal("20000000.00"))
    saldo_atual = repository.obter_saldo(1)

    print(f"\nSaldo Atual: {saldo_atual}")

    assert sacando is True
    assert isinstance(saldo_atual, Decimal)
    assert saldo_atual == saldo_anterior - Decimal("20000000.00")
    assert saldo_atual < saldo_anterior


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_depositar_dinheiro():
    repository = PessoaJuridicaRepository(db_connection_handler)

    saldo_anterior = repository.obter_saldo(3)
    print(f"\nSaldo anterior: {saldo_anterior}")
    print("Depositando...5000000.00")

    depositando = repository.depositar_dinheiro(3, Decimal("5000000.00"))
    saldo_atual = repository.obter_saldo(3)

    print(f"\nSaldo atual: {saldo_atual}")

    assert depositando is True
    assert isinstance(saldo_atual, Decimal)
    assert saldo_atual == saldo_anterior + Decimal("5000000.00")
    assert saldo_atual > saldo_anterior


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_obter_saldo():
    repository = PessoaJuridicaRepository(db_connection_handler)
    saldo_atual = repository.obter_saldo(7)

    print(f"\nSaldo atual: {saldo_atual}")

    assert saldo_atual is not None
    assert isinstance(saldo_atual, Decimal)
    assert saldo_atual >= 0


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_realizar_extrato():
    repository = PessoaJuridicaRepository(db_connection_handler)
    extrato = repository.realizar_extrato(7)

    print(f"\nExtrato: {extrato}")

    assert extrato is not None
    assert isinstance(extrato, dict)
    assert "id" in extrato
    assert "nome_fantasia" in extrato
    assert "email_corporativo" in extrato
    assert "saldo" in extrato
    assert "categoria" in extrato
    assert "criado_em" in extrato
    assert "atualizado_em" in extrato
    assert extrato["id"] == 7
    assert isinstance(extrato["saldo"], float)
    assert extrato["saldo"] >= 0


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_sacar_dinheiro_saldo_insuficiente():
    repository = PessoaJuridicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Saldo Insuficiente"):
        repository.sacar_dinheiro(1, Decimal("999999999999999.00"))


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_sacar_dinheiro_valor_zero():
    repository = PessoaJuridicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Valor de saque deve ser positivo"):
        repository.sacar_dinheiro(1, Decimal("0.00"))


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_sacar_dinheiro_valor_negativo():
    repository = PessoaJuridicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Valor de saque deve ser positivo"):
        repository.sacar_dinheiro(1, Decimal("-100.00"))


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_depositar_dinheiro_valor_zero():
    repository = PessoaJuridicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Valor de depósito deve ser positivo"):
        repository.depositar_dinheiro(1, Decimal("0.00"))


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_depositar_dinheiro_valor_negativo():
    repository = PessoaJuridicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Valor de depósito deve ser positivo"):
        repository.depositar_dinheiro(1, Decimal("-100.00"))


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_obter_saldo_empresa_inexistente():
    repository = PessoaJuridicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Empresa com ID 999 não encontrada"):
        repository.obter_saldo(999)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_realizar_extrato_empresa_inexistente():
    repository = PessoaJuridicaRepository(db_connection_handler)

    with pytest.raises(ValueError, match="Empresa com ID 999 não encontrada"):
        repository.realizar_extrato(999)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_buscar_por_categoria():
    repository = PessoaJuridicaRepository(db_connection_handler)
    categoria = repository.buscar_por_categoria("premium")

    print(f"\nLista de empresas: {categoria}")

    assert categoria is not None
    assert isinstance(categoria, list)
    assert len(categoria) > 0
    assert all(isinstance(p, PessoaJuridicaTable) for p in categoria)
    assert all(p.categoria == "premium" for p in categoria)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_buscar_por_saldo_maior_que():
    repository = PessoaJuridicaRepository(db_connection_handler)

    valor_minimo = Decimal("100000000.00")
    saldo_maior = repository.buscar_por_saldo_maior_que(valor_minimo)

    print(f"Lista de empresas: {saldo_maior}")

    assert saldo_maior is not None
    assert isinstance(saldo_maior, list)
    if len(saldo_maior) > 0:
        assert all(isinstance(p, PessoaJuridicaTable) for p in saldo_maior)
        assert all(p.saldo > valor_minimo for p in saldo_maior)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_buscar_com_faturamento_maior_que():
    repository = PessoaJuridicaRepository(db_connection_handler)

    valor_minimo = Decimal("30000000.00")
    faturamento_maior = repository.buscar_com_faturamento_maior_que(valor_minimo)

    print(f"\nLista de empresas: {faturamento_maior}")

    assert faturamento_maior is not None
    assert isinstance(faturamento_maior, list)
    if len(faturamento_maior) > 0:
        assert all(isinstance(p, PessoaJuridicaTable) for p in faturamento_maior)
        assert all(p.faturamento > valor_minimo for p in faturamento_maior)


@pytest.mark.skip(reason="integracao com o banco de dados")
def test_buscar_por_idade_empresa():
    repository = PessoaJuridicaRepository(db_connection_handler)

    idade_min = 10
    idade_max = 20
    idade_empresa = repository.buscar_por_idade_empresa(idade_min, idade_max)

    print(f"\nLista de empresas: {idade_empresa}")

    assert idade_empresa is not None
    assert isinstance(idade_empresa, list)
    if len(idade_empresa) > 0:
        assert all(isinstance(p, PessoaJuridicaTable) for p in idade_empresa)
        assert all(p.idade >= idade_min and p.idade <= idade_max for p in idade_empresa)
