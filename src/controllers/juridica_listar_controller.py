from typing import Dict, List

from src.controllers.interfaces.juridica_listar_controller import (
    PessoaJuridicaListarControllerInterface,
)
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.interfaces.pessoa_juridica_repository import (
    PessoaJuridicaRepositoryInterface,
)


class PessoaJuridicaListarController(PessoaJuridicaListarControllerInterface):
    def __init__(self, repository: PessoaJuridicaRepositoryInterface) -> None:
        self.__repository = repository

    def listar(self) -> Dict:
        try:
            pessoas = self.__find_all_pessoa_in_db()

            if not pessoas:
                return {"success": False, "error": "Nenhuma Pessoa Jurídica Cadastrada"}

            return self.__format_response(pessoas)

        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def __find_all_pessoa_in_db(self) -> List[PessoaJuridicaTable]:
        pessoas = self.__repository.listar_todas()
        if not pessoas:
            raise Exception("Nenhuma Pessoa Jurídica Cadastrada")
        return pessoas

    def __format_response(self, pessoas: List[PessoaJuridicaTable]) -> Dict:
        return {
            "data": {
                "type": "Pessoa Jurídica",
                "count": len(pessoas),
                "attributes": [
                    {
                        "nome_fantasia": pessoa.nome_fantasia,
                        "email_corporativo": pessoa.email_corporativo,
                        "celular": pessoa.celular,
                        "idade": pessoa.idade,
                        "faturamento": pessoa.faturamento,
                        "categoria": pessoa.categoria,
                        "saldo": pessoa.saldo,
                    }
                    for pessoa in pessoas
                ],
            }
        }
