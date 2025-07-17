from pydantic import BaseModel

# Entrada de login (usado implicitamente por OAuth2PasswordRequestForm)

# Token JWT de resposta
class Token(BaseModel):
    access_token: str
    token_type: str

# Dados extraídos do token
class TokenData(BaseModel):
    username: str | None = None

# Representação do usuário (opcional em retornos futuros)
class UsuarioSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True