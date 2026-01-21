import re
from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator

from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.views.http_types.http_request import HttpRequest


class PessoaJuridicaCriarSchema(BaseModel):
    nome_fantasia: str = Field(
        min_length=3, max_length=255, description="Nome fantasia da pessoa jurídica"
    )

    email_corporativo: EmailStr = Field(description="Email corporativo válido")

    celular: str = Field(min_length=10, max_length=20, description="Número do celular")

    idade: int = Field(
        ge=0, le=200, description="Tempo de atividade da empresa entre 0 e 200 anos"
    )

    faturamento: Decimal = Field(ge=0, description="Saldo inicial não negativa")

    categoria: str = Field(
        min_length=1, max_length=100, description="Categoria da empresa"
    )

    saldo: Decimal = Field(ge=0, description="Saldo inicial não negativo")

    @field_validator("celular")
    @classmethod
    def validate_celular(cls, v: str) -> str:
        # Remove carecteres não númericos e valida tamanho
        celular_limpo = re.sub(r"\D", "", v)

        if len(celular_limpo) not in [10, 11]:
            raise ValueError("Celular de deve ter 10 ou 11 dígitos (ex: 92010321031)")

        return celular_limpo

    @field_validator("nome_fantasia")
    @classmethod
    def validate_nome(cls, v: str) -> str:
        # Valida que o nome não é vazio após strip
        nome_limpo = v.strip()
        if not nome_limpo:
            raise ValueError("Nome fantasia não pode ser vazio")

        return nome_limpo

    @field_validator("categoria")
    @classmethod
    def validate_categoria(cls, v: str):
        # Valida que a categoria não é vazia
        categoria_limpa = v.strip()
        if not categoria_limpa:
            raise ValueError("Categoria não pode ser vazia")

        return categoria_limpa

    class Config:
        str_strip_whitespace = True
        validate_assignment = True


def juridica_criar_validator(http_request: HttpRequest) -> Dict:
    try:
        # Valida e converte para o schema Pydantic
        validated_data = PessoaJuridicaCriarSchema(**http_request.body)

        return validated_data.model_dump()
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = error["loc"][0]
            message = error["msg"]
            errors.append(f"{field}: {message}")

        error_message = "; ".join(errors)
        raise HttpBadRequestError(error_message) from e
