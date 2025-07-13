from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class FaturamentoMensal(Base):
    __tablename__ = "faturamento_mensal"

    id = Column(Integer, primary_key=True)
    mes_referencia = Column(String(10), unique=True, nullable=False)  # Ex: "Jan/25"
    ordem_cronologica = Column(Integer, unique=True, nullable=False)  # Ex: 202501 para Jan/25
    faturamento = Column(Float, default=0.0)
    evolucao_percentual = Column(Float, default=0.0)  # Calculado em relação ao mês anterior
    criado_em = Column(DateTime(timezone=True), server_default=func.now())