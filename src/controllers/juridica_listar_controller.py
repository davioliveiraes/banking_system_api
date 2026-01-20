from typing import Dict, List

from src.controllers.interfaces.juridica_listar_controller import (
    PessoaJuridicaListarControllerInterface,
)
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.interfaces.pessoa_juridica_repository import (
    PessoaJuridicaRepositoryInterface,
)


class PessoaJuridicaListarController(PessoaJuridicaListarControllerInterface):
    def __init__(self, repository: PessoaJuridicaRepositoryInterface) -> None:
        self.__repository = repository

    def listar(self) -> Dict:
        pessoas = self.__find_all_pessoa_in_db()
        return self.__format_response(pessoas)

    def __find_all_pessoa_in_db(self) -> List[PessoaJuridicaTable]:
        pessoas = self.__repository.listar_todas()
        if not pessoas:
            raise HttpNotFoundError("Nenhuma Pessoa Jurídica Cadastrada")
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
