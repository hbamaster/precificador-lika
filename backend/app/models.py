from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

class ConfigBling(Base):
    __tablename__ = "config_bling"
    
    id = Column(Integer, primary_key=True, index=True)
    apikey_encrypted = Column(Text, nullable=False)
    versao_api = Column(String(10), default="v1")
    ultimo_status = Column(Boolean, default=None)
    ultimo_teste_em = Column(DateTime(timezone=True), default=None)
    ultimo_mensagem = Column(Text, default=None)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())