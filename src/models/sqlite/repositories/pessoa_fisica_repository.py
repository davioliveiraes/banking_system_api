from decimal import Decimal
from typing import List, Optional

from sqlalchemy.exc import NoResultFound

from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.interfaces.pessoa_fisica_repository import (
    PessoaFisicaRepositoryInterface,
)


class PessoaFisicaRepository(PessoaFisicaRepositoryInterface):
    """
    Repository para operações de banco de dados da entidade Pessoa Física.

    Responsabilidades:
        - CRUD (Create, Read, Update, Delete)
        - Queries específicas (buscar por email, CPF, etc)
        - Operações de saldo (saque, depósito, transferência)
    """

    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    # CRUD BÁSICO

    def criar_pessoa(self, pessoa_data: dict) -> PessoaFisicaTable:
        with self.__db_connection as database:
            nova_pessoa = PessoaFisicaTable(**pessoa_data)
            database.session.add(nova_pessoa)
            database.session.commit()
            database.session.refresh(nova_pessoa)
            return nova_pessoa

    def buscar_por_id(self, pessoa_id: int) -> Optional[PessoaFisicaTable]:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_id)
                    .one()
                )
                return pessoa
            except NoResultFound:
                return None

    def buscar_por_email(self, email: str) -> Optional[PessoaFisicaTable]:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.email == email)
                    .one()
                )
                return pessoa
            except NoResultFound:
                return None

    def buscar_por_celular(self, celular: str) -> Optional[PessoaFisicaTable]:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.celular == celular)
                    .one()
                )
                return pessoa
            except NoResultFound:
                return None

    def listar_todas(self) -> List[PessoaFisicaTable]:
        with self.__db_connection as database:
            return database.session.query(PessoaFisicaTable).all()

    def atualizar_pessoa(
        self, pessoa_id: int, dados_atualizacao: dict
    ) -> Optional[PessoaFisicaTable]:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_id)
                    .one()
                )

                campos_permitidos = {
                    "nome_completo",
                    "email",
                    "celular",
                    "categoria",
                    "renda_mensal",
                    "idade",
                }

                for campo, valor in dados_atualizacao.items():
                    if campo in campos_permitidos and hasattr(pessoa, campo):
                        setattr(pessoa, campo, valor)

                database.session.commit()
                database.session.refresh(pessoa)
                return pessoa

            except NoResultFound:
                return None

    def deletar_pessoa(self, pessoa_id: int) -> bool:
        with self.__db_connection as database:
            rows_deleted = (
                database.session.query(PessoaFisicaTable)
                .filter(PessoaFisicaTable.id == pessoa_id)
                .delete()
            )
            database.session.commit()
            return rows_deleted > 0

    # Operações Bancárias

    def sacar_dinheiro(self, pessoa_id: int, valor: Decimal) -> bool:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_id)
                    .one()
                )
            except NoResultFound as exc:
                raise ValueError(f"Pessoa com ID {pessoa_id} não encontrada") from exc

            if valor <= 0:
                raise ValueError("Valor de saque deve ser positivo")

            if pessoa.saldo < valor:
                raise ValueError(
                    f"Saldo Insuficiente. Saldo: {pessoa.saldo}, Saque: {valor}"
                )

            pessoa.saldo -= valor
            database.session.commit()
            return True

    def depositar_dinheiro(self, pessoa_id: int, valor: Decimal) -> bool:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_id)
                    .one()
                )
            except NoResultFound as exc:
                raise ValueError(
                    f"Pessoa com ID {pessoa_id} não foi encontrada"
                ) from exc

            if valor <= 0:
                raise ValueError("Valor de depósito deve ser positivo.")

            pessoa.saldo += valor
            database.session.commit()
            return True

    def obter_saldo(self, pessoa_id: int) -> Decimal:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable.saldo)
                    .filter(PessoaFisicaTable.id == pessoa_id)
                    .one()
                )
                return pessoa.saldo
            except NoResultFound as exc:
                raise ValueError(f"Pessoa com ID {pessoa_id} não encontrada") from exc

    def realizar_extrato(self, pessoa_id: int) -> dict:
        with self.__db_connection as database:
            try:
                pessoa = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_id)
                    .one()
                )

                return {
                    "id": pessoa.id,
                    "nome_completo": pessoa.nome_completo,
                    "email": pessoa.email,
                    "saldo": float(pessoa.saldo),
                    "categoria": pessoa.categoria,
                    "criado_em": pessoa.criado_em,
                    "atualizado_em": pessoa.atualizado_em,
                }
            except NoResultFound as exc:
                raise ValueError(f"Pessoa com ID {pessoa_id} não encontrada") from exc

    # Queries(Consultas) Específicas

    def buscar_por_categoria(self, categoria: str) -> List[PessoaFisicaTable]:
        with self.__db_connection as database:
            pessoas = (
                database.session.query(PessoaFisicaTable)
                .filter(PessoaFisicaTable.categoria == categoria)
                .all()
            )
            return pessoas

    def buscar_com_saldo_maior_que(self, valor: Decimal) -> List[PessoaFisicaTable]:
        with self.__db_connection as database:
            pessoas = (
                database.session.query(PessoaFisicaTable)
                .filter(PessoaFisicaTable.saldo > valor)
                .all()
            )
            return pessoas
