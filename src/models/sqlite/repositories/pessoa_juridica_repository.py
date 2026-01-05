from decimal import Decimal
from typing import List, Optional

from sqlalchemy.exc import NoResultFound

from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.interfaces.pessoa_juridica_repository import (
    PessoaJuridicaRepositoryInterface,
)


class PessoaJuridicaRepository(PessoaJuridicaRepositoryInterface):
    """
    Repository para operações de banco de dados de entidade

    Responsabilidades:
        - CRUD (Create, Read, Update, Delete)
        - Queries específicas (buscar por email corporativo, CNPJ, etc)
        - Operações de saldo (saque, depósito, transferência)
    """

    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    # CRUD BÁSICO

    def criar_empresa(self, empresa_data: dict) -> PessoaJuridicaTable:
        with self.__db_connection as database:
            nova_empresa = PessoaJuridicaTable(**empresa_data)
            database.session.add(nova_empresa)
            database.session.commit()
            database.session.refresh(nova_empresa)
            return nova_empresa

    def buscar_por_id(self, empresa_id: int) -> Optional[PessoaJuridicaTable]:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == empresa_id)
                    .one()
                )
                return empresa
            except NoResultFound:
                return None

    def buscar_por_email_corporativo(self, email: str) -> Optional[PessoaJuridicaTable]:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.email_corporativo == email)
                    .one()
                )
                return empresa
            except NoResultFound:
                return None

    def buscar_por_celular(self, celular: str) -> Optional[PessoaJuridicaTable]:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.celular == celular)
                    .one()
                )
                return empresa
            except NoResultFound:
                return None

    def listar_todas(self) -> List[PessoaJuridicaTable]:
        with self.__db_connection as database:
            return database.session.query(PessoaJuridicaTable).all()

    def atualizar_empresa(
        self, empresa_id: int, dados_atualizacao: dict
    ) -> Optional[PessoaJuridicaTable]:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == empresa_id)
                    .one()
                )

                campos_permitidos = {
                    "nome_fantasia",
                    "email_corporativo",
                    "celular",
                    "categoria",
                    "faturamento",
                    "idade",
                }

                for campo, valor in dados_atualizacao.items():
                    if campo in campos_permitidos and hasattr(empresa, campo):
                        setattr(empresa, campo, valor)

                database.session.commit()
                database.session.refresh(empresa)
                return empresa

            except NoResultFound:
                return None

    def deletar_empresa(self, empresa_id: int) -> bool:
        with self.__db_connection as database:
            rows_deleted = (
                database.session.query(PessoaJuridicaTable)
                .filter(PessoaJuridicaTable.id == empresa_id)
                .delete()
            )
            database.session.commit()
            return rows_deleted > 0

    # OPERAÇÕES BANCÁRIAS

    def sacar_dinheiro(self, empresa_id: int, valor: Decimal) -> bool:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == empresa_id)
                    .one()
                )
            except NoResultFound as exc:
                raise ValueError(f"Empresa com ID {empresa_id} não encontrada") from exc

            if valor <= 0:
                raise ValueError("Valor de saque deve ser positivo")

            if empresa.saldo < valor:
                raise ValueError(
                    f"Saldo Insuficiente. Saldo: {empresa.saldo}, Saque: {valor}"
                )

            empresa.saldo -= valor
            database.session.commit()
            return True

    def depositar_dinheiro(self, empresa_id: int, valor: Decimal) -> bool:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == empresa_id)
                    .one()
                )
            except NoResultFound as exc:
                raise ValueError(f"Empresa com ID {empresa_id} não encontrada") from exc

            if valor <= 0:
                raise ValueError("Valor de depósito deve ser positivo")

            empresa.saldo += valor
            database.session.commit()
            return True

    def obter_saldo(self, empresa_id: int) -> Decimal:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable.saldo)
                    .filter(PessoaJuridicaTable.id == empresa_id)
                    .one()
                )
                return empresa.saldo
            except NoResultFound as exc:
                raise ValueError(f"Empresa com ID {empresa_id} não encontrada") from exc

    def realizar_extrato(self, empresa_id: int) -> dict:
        with self.__db_connection as database:
            try:
                empresa = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == empresa_id)
                    .one()
                )

                return {
                    "id": empresa.id,
                    "nome_fantasia": empresa.nome_fantasia,
                    "email_corporativo": empresa.email_corporativo,
                    "saldo": float(empresa.saldo),
                    "categoria": empresa.categoria,
                    "idade": empresa.idade,
                    "criado_em": empresa.criado_em,
                    "atualizado_em": empresa.atualizado_em,
                }
            except NoResultFound as exc:
                raise ValueError(f"Empresa com ID {empresa_id} não encontrada") from exc

    # Queries(Consultas) Específicas

    def buscar_por_categoria(self, categoria: str) -> List[PessoaJuridicaTable]:
        with self.__db_connection as database:
            empresas = (
                database.session.query(PessoaJuridicaTable)
                .filter(PessoaJuridicaTable.categoria == categoria)
                .all()
            )

            return empresas

    def buscar_por_saldo_maior_que(self, valor: Decimal) -> List[PessoaJuridicaTable]:
        with self.__db_connection as database:
            empresas = (
                database.session.query(PessoaJuridicaTable)
                .filter(PessoaJuridicaTable.saldo > valor)
                .all()
            )

            return empresas

    def buscar_com_faturamento_maior_que(
        self, valor: Decimal
    ) -> List[PessoaJuridicaTable]:
        with self.__db_connection as database:
            empresas = (
                database.session.query(PessoaJuridicaTable)
                .filter(PessoaJuridicaTable.faturamento > valor)
                .all()
            )

            return empresas

    def buscar_por_idade_empresa(
        self, idade_min: int, idade_max: int
    ) -> List[PessoaJuridicaTable]:
        with self.__db_connection as database:
            empresas = (
                database.session.query(PessoaJuridicaTable)
                .filter(
                    PessoaJuridicaTable.idade >= idade_min,
                    PessoaJuridicaTable.idade <= idade_max,
                )
                .all()
            )

            return empresas
