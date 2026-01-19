import re
from typing import Dict

from src.controllers.interfaces.juridica_criar_controller import (
    PessoaJuridicaCriarControllerInterface,
)
from src.models.sqlite.interfaces.pessoa_juridica_repository import (
    PessoaJuridicaRepositoryInterface,
)


class PessoaJuridicaCriarControler(PessoaJuridicaCriarControllerInterface):
    def __init__(self, repository: PessoaJuridicaRepositoryInterface):
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
            "nome_fantasia",
            "email_corporativo",
            "celular",
            "categoria",
            "faturamento",
            "idade",
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
        # Idade da empresa
        if not isinstance(pessoa_data["idade"], int):
            raise ValueError("Idade da empresa deve ser um número inteiro")
        if pessoa_data["idade"] < 0:
            raise ValueError("Idade da empresa não deve ser negativa")
        if pessoa_data["idade"] > 200:
            raise ValueError("Idade da empresa inválida")

        # Email corporativo
        email = pessoa_data["email_corporativo"]
        padrao_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(padrao_email, email):
            raise ValueError("Email corporativo inválido")

        # Celular
        celular = str(pessoa_data["celular"]).strip()
        celular_limpo = re.sub(r"\D", "", celular)
        if len(celular_limpo) not in [10, 11]:
            raise ValueError("Celular deve ter 10 ou 11 dígitos")

        # Valores monetários
        try:
            faturamento = float(pessoa_data["faturamento"])
            saldo = float(pessoa_data["saldo"])
        except (ValueError, TypeError) as exc:
            raise ValueError(
                "O faturamento e o saldo deve ser valores numéricos válidos"
            ) from exc

        if faturamento < 0:
            raise ValueError("O faturamento não pode ser um valor negativo")
        if saldo < 0:
            raise ValueError("O saldo não pode ser um valor negativo")

    def __insert_pessoa_in_db(self, pessoa_data: Dict):
        return self.__repository.criar_empresa(pessoa_data)

    def __format_response(self, pessoa_obj) -> Dict:
        pessoa_dict = {
            "nome_fantasia": pessoa_obj.nome_fantasia,
            "email_corporativo": pessoa_obj.email_corporativo,
            "celular": pessoa_obj.celular,
            "categoria": pessoa_obj.categoria,
            "faturamento": float(pessoa_obj.faturamento),
            "idade": pessoa_obj.idade,
            "saldo": float(pessoa_obj.saldo),
            "criado_em": (
                pessoa_obj.criado_em.isoformat() if pessoa_obj.criado_em else None
            ),
            "atualizado_em": (
                pessoa_obj.atualizado_em.isoformat()
                if pessoa_obj.atualizado_em
                else None
            ),
        }

        return {
            "success": True,
            "data": {"type": "Pessoa Jurídica", "count": 1, "attributes": pessoa_dict},
        }
