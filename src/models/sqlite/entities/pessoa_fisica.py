from datetime import datetime
from sqlalchemy import Column, String, BIGINT, NUMERIC, INT, DateTime, CheckConstraint
from src.models.sqlite.settings.base import Base

class PessoaFisicaTable(Base):
    __tablename__ = "pessoa_fisica"

    id = Column(BIGINT, primary_key=True)
    renda_mensal = Column(NUMERIC(10, 2), nullable=False)
    idade = Column(INT, nullable=False)
    nome_completo = Column(String(200), nullable=False, index=True)
    celular = Column(String(15), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    categoria = Column(String(50), nullable=False)
    saldo = Column(NUMERIC(15, 2), nullable=False, default=0.0)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('idade >= 18', name='check_idade_minima'),
        CheckConstraint('renda_mensal >= 0', name='check_renda_positiva'),
        CheckConstraint('saldo >= 0', name='check_saldo_positivo'),
    )

    def __repr__(self):
        return f"Pessoa Física: [id={self.id}, nome_completo={self.nome_completo}]"
