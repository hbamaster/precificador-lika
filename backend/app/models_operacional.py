from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class CategoriaCusto(Base):
    __tablename__ = "categoria_custo"

    id = Column(Integer, primary_key=True)
    tipo = Column(String(20))  # "despesa" ou "investimento"
    nome = Column(String(100), nullable=False)
    ordem = Column(Integer, default=0)

    subcategorias = relationship("SubcategoriaCusto", back_populates="categoria", cascade="all, delete")

class SubcategoriaCusto(Base):
    __tablename__ = "subcategoria_custo"

    id = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey("categoria_custo.id"))
    nome = Column(String(100), nullable=False)
    ordem = Column(Integer, default=0)

    categoria = relationship("CategoriaCusto", back_populates="subcategorias")
    lancamentos = relationship("LancamentoCusto", back_populates="subcategoria", cascade="all, delete")

class LancamentoCusto(Base):
    __tablename__ = "lancamento_custo"

    id = Column(Integer, primary_key=True)
    subcategoria_id = Column(Integer, ForeignKey("subcategoria_custo.id"))
    nome = Column(String(100), nullable=False)
    valor_mensal = Column(Float, default=0.0)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    subcategoria = relationship("SubcategoriaCusto", back_populates="lancamentos")