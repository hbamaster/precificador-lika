from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from .database import Base

class SimplesNacionalFaixa(Base):
    __tablename__ = "simples_nacional_faixa"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    faturamento_inicio = Column(Float, nullable=False)
    faturamento_fim = Column(Float, nullable=False)
    aliquota = Column(Float, nullable=False)
    deducao = Column(Float, nullable=False)

    reparticao = relationship("SimplesNacionalReparticao", back_populates="faixa", uselist=False, cascade="all, delete")

class SimplesNacionalReparticao(Base):
    __tablename__ = "simples_nacional_reparticao"

    id = Column(Integer, primary_key=True)
    faixa_id = Column(Integer, ForeignKey("simples_nacional_faixa.id"), unique=True)

    irpj = Column(Float, nullable=False)
    csll = Column(Float, nullable=False)
    cofins = Column(Float, nullable=False)
    pis = Column(Float, nullable=False)
    cpp = Column(Float, nullable=False)
    icms = Column(Float, nullable=False)

    faixa = relationship("SimplesNacionalFaixa", back_populates="reparticao")