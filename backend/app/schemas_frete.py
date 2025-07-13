from pydantic import BaseModel
from typing import Optional

class FreteEntrada(BaseModel):
    marketplace: str
    modalidade: str
    peso: float
    preco_produto: float
    categoria: Optional[str] = None
    nivel_logistico: Optional[str] = None

class FreteSaida(BaseModel):
    valor: float