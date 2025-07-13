from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoriaCustoBase(BaseModel):
    nome: str
    tipo: str  # "despesa" ou "investimento"
    ordem: Optional[int] = 0

class CategoriaCustoCreate(CategoriaCustoBase):
    pass

class CategoriaCustoOut(CategoriaCustoBase):
    id: int
    class Config:
        from_attributes = True

class SubcategoriaCustoBase(BaseModel):
    nome: str
    ordem: Optional[int] = 0
    categoria_id: int

class SubcategoriaCustoCreate(SubcategoriaCustoBase):
    pass

class SubcategoriaCustoOut(SubcategoriaCustoBase):
    id: int
    class Config:
        from_attributes = True

class LancamentoCustoBase(BaseModel):
    nome: str
    valor_mensal: Optional[float] = 0.0
    observacao: Optional[str] = None
    subcategoria_id: int

class LancamentoCustoCreate(LancamentoCustoBase):
    pass

class LancamentoCustoOut(LancamentoCustoBase):
    id: int
    criado_em: datetime
    class Config:
        from_attributes = True

class TotaisOperacionais(BaseModel):
    total_despesas: float
    total_investimentos: float
    total_geral: float