# pylint: disable=duplicate-code
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable


class PessoaJuridicaRepositoryInterface(ABC):

    # CRUD BÁSICO
    @abstractmethod
    def criar_empresa(self, empresa_data: dict) -> PessoaJuridicaTable:
        pass

    @abstractmethod
    def buscar_por_id(self, empresa_id: int) -> Optional[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def buscar_por_email_corporativo(self, email: str) -> Optional[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def buscar_por_celular(self, celular: str) -> Optional[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def listar_todas(self) -> List[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def atualizar_empresa(
        self, empresa_id: int, dados_atualizacao: dict
    ) -> Optional[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def deletar_empresa(self, empresa_id: int) -> bool:
        pass

    # OPERAÇÕES BANCÁRIAS
    @abstractmethod
    def sacar_dinheiro(self, empresa_id: int, valor: Decimal) -> bool:
        pass

    @abstractmethod
    def depositar_dinheiro(self, empresa_id: int, valor: Decimal) -> bool:
        pass

    @abstractmethod
    def obter_saldo(self, empresa_id: int) -> Decimal:
        pass

    @abstractmethod
    def realizar_extrato(self, empresa_id: int) -> dict:
        pass

    # CONSULTAS ESPECÍFICAS
    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> List[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def buscar_por_saldo_maior_que(self, valor: Decimal) -> List[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def buscar_com_faturamento_maior_que(
        self, valor: Decimal
    ) -> List[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def buscar_por_idade_empresa(
        self, idade_min: int, idade_max: int
    ) -> List[PessoaJuridicaTable]:
        pass
