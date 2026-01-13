from abc import ABC, abstractmethod
from typing import Dict


class PessoaJuridicaListarControllerInterface(ABC):

    @abstractmethod
    def listar(self) -> Dict:
        pass
