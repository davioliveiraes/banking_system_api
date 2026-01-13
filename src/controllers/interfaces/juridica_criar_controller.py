from abc import ABC, abstractmethod
from typing import Dict


class PessoaJuridicaCriarControllerInterface(ABC):

    @abstractmethod
    def criar(self, pessoa_data: Dict):
        pass
