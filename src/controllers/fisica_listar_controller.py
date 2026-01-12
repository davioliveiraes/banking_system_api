from typing import Dict

from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.interfaces.pessoa_fisica_repository import (
    PessoaFisicaRepositoryInterface,
)


class PessoaFisicaListarController:
    def __init__(self, repository: PessoaFisicaRepositoryInterface) -> None:
        self.__repository = repository

    def listar(self, pessoa_fisica_id: int) -> Dict:
        try:
            pessoa_fisica = self.__find_pessoa_in_db(pessoa_fisica_id)
            return self.__format_response(pessoa_fisica)
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def __find_pessoa_in_db(self, pessoa_fisica_id: int) -> PessoaFisicaTable:
        pessoa_fisica = self.__repository.buscar_por_id(pessoa_fisica_id)
        if not pessoa_fisica:
            raise Exception("Pessoa Física não encontrada")
        return pessoa_fisica

    def __format_response(self, pessoa_fisica: PessoaFisicaTable) -> Dict:
        return {
            "data": {
                "type": "Pessoa Física",
                "count": 1,
                "attributes": {
                    "nome_completo": pessoa_fisica.nome_completo,
                    "email": pessoa_fisica.email,
                    "celular": pessoa_fisica.celular,
                    "idade": pessoa_fisica.idade,
                    "renda_mensal": pessoa_fisica.renda_mensal,
                    "categoria": pessoa_fisica.categoria,
                    "saldo": pessoa_fisica.saldo,
                },
            }
        }
