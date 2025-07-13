from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class MargemCanal(Base):
    __tablename__ = "margem_canal"

    id = Column(Integer, primary_key=True)
    canal = Column(String(100), unique=True, nullable=False)
    margem_desejada = Column(Float, default=0.0)  # Percentual desejado
    margem_observada = Column(Float, default=0.0)  # Calculado futuramente
    inativo = Column(Boolean, default=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())