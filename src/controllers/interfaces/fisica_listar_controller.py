from abc import ABC, abstractmethod
from typing import Dict


class PessoaFisicaListarControllerInterface(ABC):

    @abstractmethod
    def listar(self) -> Dict:
        pass
