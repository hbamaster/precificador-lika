from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Formato de retorno do token JWT
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

# Dados enviados pelo usuário ao fazer login
class LoginForm(BaseModel):
    username: str
    password: str

# Configuração recebida para salvar chave do Bling
class ConfigBlingIn(BaseModel):
    apikey: str
    versao_api: Optional[str] = "v1"

# Dados retornados ao consultar configuração do Bling
class ConfigBlingOut(BaseModel):
    apikey: str
    versao_api: str
    ultimo_status: Optional[bool]
    ultimo_teste_em: Optional[datetime]
    ultimo_mensagem: Optional[str]

    class Config:
        orm_mode = True


from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class CategoriaEnum(str, Enum):
    NORMAL = "normal"
    ANIMAL = "animal"
    ESPECIAL = "especial"

class FreteEntrada(BaseModel):
    """
    Schema para cálculo de frete.
    
    Campos obrigatórios:
    - marketplace: Plataforma (mercadolivre, amazon, etc.)
    - modalidade: Tipo de frete (full, dba, etc.)
    - peso: Em kg (valor positivo)
    - preco_produto: Valor monetário (positivo)
    """
    marketplace: str = Field(..., min_length=3, max_length=50)
    modalidade: str = Field(..., min_length=2, max_length=20)
    peso: float = Field(..., gt=0, description="Peso em quilogramas")
    preco_produto: float = Field(..., gt=0, description="Preço do produto")
    categoria: Optional[CategoriaEnum] = Field(None, description="Categoria especial")
    nivel_logistico: Optional[str] = Field(None, max_length=10)

    class Config:
        json_schema_extra = {
            "example": {
                "marketplace": "mercadolivre",
                "modalidade": "full",
                "peso": 1.5,
                "preco_produto": 150.99,
                "categoria": "normal"
            }
        }

class FreteSaida(BaseModel):
    valor: float = Field(..., description="Valor calculado do frete")