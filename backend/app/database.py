from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Cria engine a partir do DATABASE_URL do .env
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Cria sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter sessão em endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()