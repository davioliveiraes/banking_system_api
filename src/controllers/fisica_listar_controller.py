from typing import Dict, List

from src.controllers.interfaces.fisica_listar_controller import (
    PessoaFisicaListarControllerInterface,
)
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.interfaces.pessoa_fisica_repository import (
    PessoaFisicaRepositoryInterface,
)


class PessoaFisicaListarController(PessoaFisicaListarControllerInterface):
    def __init__(self, repository: PessoaFisicaRepositoryInterface) -> None:
        self.__repository = repository

    def listar(self) -> Dict:
        pessoas = self.__find_all_pessoas_in_db()
        return self.__format_response(pessoas)

    def __find_all_pessoas_in_db(self) -> List[PessoaFisicaTable]:
        pessoas = self.__repository.listar_todas()
        if not pessoas:
            raise HttpNotFoundError("Nenhuma Pessoa Física Cadastrada")
        return pessoas

    def __format_response(self, pessoas: List[PessoaFisicaTable]) -> Dict:
        return {
            "data": {
                "type": "Pessoa Física",
                "count": len(pessoas),
                "attributes": [
                    {
                        "nome_completo": pessoa.nome_completo,
                        "email": pessoa.email,
                        "celular": pessoa.celular,
                        "idade": pessoa.idade,
                        "renda_mensal": pessoa.renda_mensal,
                        "categoria": pessoa.categoria,
                        "saldo": pessoa.saldo,
                    }
                    for pessoa in pessoas
                ],
            }
        }
