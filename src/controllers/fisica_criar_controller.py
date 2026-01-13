import re
from typing import Dict

from src.controllers.interfaces.fisica_criar_controller import (
    PessoaFisicaCriarControllerInterface,
)
from src.models.sqlite.interfaces.pessoa_fisica_repository import (
    PessoaFisicaRepositoryInterface,
)


class PessoaFisicaCriarController(PessoaFisicaCriarControllerInterface):
    def __init__(self, repository: PessoaFisicaRepositoryInterface):
        self.__repository = repository

    def criar(self, pessoa_data: Dict) -> Dict:
        try:
            self.__validate_all_exists(pessoa_data)
            self.__validate_values(pessoa_data)
            pessoa_criada = self.__insert_pessoa_in_db(pessoa_data)
            return self.__format_response(pessoa_criada)

        except ValueError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Error inesperado: {str(e)}"}

    def __validate_all_exists(self, pessoa_data: Dict):
        campos_obrigatorios = [
            "nome_completo",
            "email",
            "celular",
            "idade",
            "renda_mensal",
            "categoria",
            "saldo",
        ]

        for campo in campos_obrigatorios:
            if campo not in pessoa_data:
                raise ValueError(f"Campo '{campo}' é obrigatório")

            valor = pessoa_data[campo]
            if valor is None:
                raise ValueError(f"Campo '{campo}' não pode ser nulo")

            if isinstance(valor, str) and valor.strip() == "":
                raise ValueError(f"Campo '{campo}' não pode ser vazio")

    def __validate_values(self, pessoa_data: Dict) -> None:
        # Idade
        if not isinstance(pessoa_data["idade"], int):
            raise ValueError("Idade deve ser um número inteiro")
        if pessoa_data["idade"] < 18:
            raise ValueError("Idade mínima é de 18 anos")
        if pessoa_data["idade"] > 120:
            raise ValueError("Idade inválida")

        # Email
        email = pessoa_data["email"]
        padrao_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(padrao_email, email):
            raise ValueError("Email inválido")

        # Nome
        if len(pessoa_data["nome_completo"].strip()) < 3:
            raise ValueError("O nome não deve ter menos que 3 caracteres")

        # Celular
        celular = str(pessoa_data["celular"]).strip()
        celular_limpo = re.sub(r"\D", "", celular)
        if len(celular_limpo) not in [10, 11]:
            raise ValueError("Celular deve ter 10 ou 11 dígitos (ex: 11987654321)")

        # Valores Monetários
        try:
            renda = float(pessoa_data["renda_mensal"])
            saldo = float(pessoa_data["saldo"])
        except (ValueError, TypeError) as exc:
            raise ValueError(
                "Renda mensal e saldo devem ser valores numéricos válidos"
            ) from exc

        if renda < 0:
            raise ValueError("Renda mensal não pode ser negativo")
        if saldo < 0:
            raise ValueError("Saldo não pode ser negativa")

    def __insert_pessoa_in_db(self, pessoa_data: Dict):
        return self.__repository.criar_pessoa(pessoa_data)

    def __format_response(self, pessoa_data: Dict) -> Dict:
        return {
            "success": True,
            "data": {"type": "Pessoa Física", "count": 1, "attributes": pessoa_data},
        }
