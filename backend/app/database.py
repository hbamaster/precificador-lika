import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from cryptography.fernet import Fernet
from typing import Generator

# Configuração do ambiente
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Validação de variáveis essenciais
required_vars = ['DATABASE_URL', 'FERNET_KEY', 'JWT_SECRET']
if missing_vars := [var for var in required_vars if not os.getenv(var)]:
    raise RuntimeError(f"Variáveis de ambiente faltando: {', '.join(missing_vars)}")

# Configuração do Fernet
try:
    fernet = Fernet(os.getenv("FERNET_KEY").encode())
except Exception as e:
    raise RuntimeError(f"Falha na configuração do Fernet: {str(e)}")

# Engine do banco de dados
engine = create_engine(
    os.getenv("DATABASE_URL"),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={"check_same_thread": False} if "sqlite" in os.getenv("DATABASE_URL", "") else {}
)

# Configuração da sessão
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()

def get_db() -> Generator:
    """Gera sessões do banco de dados com tratamento seguro"""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)