from typing import Dict, List

from src.controllers.interfaces.fisica_listar_controller import (
    PessoaFisicaListarControllerInterface,
)
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.interfaces.pessoa_fisica_repository import (
    PessoaFisicaRepositoryInterface,
)


class PessoaFisicaListarController(PessoaFisicaListarControllerInterface):
    def __init__(self, repository: PessoaFisicaRepositoryInterface) -> None:
        self.__repository = repository

    def listar(self) -> Dict:
        try:
            pessoas = self.__find_all_pessoas_in_db()

            if not pessoas:
                return {"success": False, "error": "Nenhuma Pessoa Física Cadastrada"}

            return self.__format_response(pessoas)

        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def __find_all_pessoas_in_db(self) -> List[PessoaFisicaTable]:
        pessoas = self.__repository.listar_todas()
        if not pessoas:
            raise Exception("Nenhuma Pessoa Física Cadastrada")
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
