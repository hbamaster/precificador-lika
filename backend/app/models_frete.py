from sqlalchemy import Column, Integer, String, Float
from app.database import Base


# 🔹 Mercado Livre — faixas por modalidade, categoria e faixa de preço
class FreteMercadoLivre(Base):
    __tablename__ = "fretes_mercadolivre"

    id = Column(Integer, primary_key=True, index=True)
    modalidade = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    faixa_preco = Column(String, nullable=False)
    peso_min = Column(Float, nullable=False)
    peso_max = Column(Float, nullable=False)
    valor_frete = Column(Float, nullable=False)


# 🔹 Magalu — por nível logístico e faixa de peso
class FreteMagalu(Base):
    __tablename__ = "fretes_magalu"

    id = Column(Integer, primary_key=True, index=True)
    nivel_logistico = Column(String, nullable=False)
    peso_min = Column(Float, nullable=False)
    peso_max = Column(Float, nullable=False)
    valor_frete = Column(Float, nullable=False)


# 🔹 Amazon — por modalidade e faixa de preço
class FreteAmazon(Base):
    __tablename__ = "fretes_amazon"

    id = Column(Integer, primary_key=True, index=True)
    modalidade = Column(String, nullable=False)  # DBA, FBA, FBA On-Site
    faixa_preco = Column(String, nullable=False)
    peso_min = Column(Float, nullable=False)
    peso_max = Column(Float, nullable=False)
    valor_frete = Column(Float, nullable=False)