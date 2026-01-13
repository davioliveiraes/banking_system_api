from abc import ABC, abstractmethod
from typing import Dict


class PessoaFisicaCriarControllerInterface(ABC):

    @abstractmethod
    def criar(self, pessoa_data: Dict):
        pass
