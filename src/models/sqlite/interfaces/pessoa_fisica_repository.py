# pylint: disable=duplicate-code
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable


class PessoaFisicaRepositoryInterface(ABC):

    # CRUD BÁSICO
    @abstractmethod
    def criar_pessoa(self, pessoa_data: dict) -> PessoaFisicaTable:
        pass

    @abstractmethod
    def buscar_por_id(self, pessoa_id: int) -> Optional[PessoaFisicaTable]:
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[PessoaFisicaTable]:
        pass

    @abstractmethod
    def buscar_por_celular(self, celular: str) -> Optional[PessoaFisicaTable]:
        pass

    @abstractmethod
    def listar_todas(self) -> List[PessoaFisicaTable]:
        pass

    @abstractmethod
    def atualizar_pessoa(
        self, pessoa_id: int, dados_atualizacao: dict
    ) -> Optional[PessoaFisicaTable]:
        pass

    @abstractmethod
    def deletar_pessoa(self, pessoa_id: int) -> bool:
        pass

    # OPERAÇÕES BANCÁRIAS
    @abstractmethod
    def sacar_dinheiro(self, pessoa_id: int, valor: Decimal) -> bool:
        pass

    @abstractmethod
    def depositar_dinheiro(self, pessoa_id: int, valor: Decimal) -> bool:
        pass

    @abstractmethod
    def obter_saldo(self, pessoa_id: int) -> Decimal:
        pass

    @abstractmethod
    def realizar_extrato(self, pessoa_id: int) -> dict:
        pass

    # CONSULTAS ESPECÍFICAS
    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> List[PessoaFisicaTable]:
        pass

    @abstractmethod
    def buscar_com_saldo_maior_que(self, valor: Decimal) -> List[PessoaFisicaTable]:
        pass
