from pydantic import BaseSettings, Field, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    # Segurança
    SECRET_KEY: str = Field(..., description="Chave secreta para geração de tokens JWT")
    ALGORITHM: str = Field(default="HS256", description="Algoritmo de assinatura do token")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, description="Expiração do token em minutos")

    # Banco de dados
    DATABASE_URL: str = Field(..., description="URL de conexão com PostgreSQL")

    # CORS
    ALLOWED_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "https://precificador-site.onrender.com"
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instância global
settings = Settings()