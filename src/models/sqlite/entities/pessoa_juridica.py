from datetime import datetime
from sqlalchemy import Column, String, BIGINT, NUMERIC, INT, DateTime, CheckConstraint
from src.models.sqlite.settings.base import Base

class PessoaJuridicaTable(Base):
    __tablename__ = "pessoa_juridica"

    id = Column(BIGINT, primary_key=True)
    faturamento = Column(NUMERIC(10, 2), nullable=False)
    idade = Column(INT, nullable=False)
    nome_fantasia = Column(String(200), nullable=False, index=True)
    celular = Column(String(15), nullable=False, unique=True)
    email_corporativo = Column(String(150), nullable=False, unique=True)
    categoria = Column(String(50), nullable=False)
    saldo = Column(NUMERIC(15, 2), nullable=False, default=0.0)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('idade >= 0', name='check_idade_minima'),
        CheckConstraint('faturamento >= 0', name='check_faturamento_positivo'),
        CheckConstraint('saldo >= 0', name='check_saldo_positivo'),
    )

    def __repr__(self):
        return f"Pessoa Jurídica: [id={self.id}, nome_fantasia={self.nome_fantasia}]"
