from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FaturamentoMensalBase(BaseModel):
    mes_referencia: str             # Ex: "Jan/25"
    ordem_cronologica: int          # Ex: 202501 para Jan/25
    faturamento: float

class FaturamentoMensalCreate(FaturamentoMensalBase):
    pass

class FaturamentoMensalOut(FaturamentoMensalBase):
    id: int
    evolucao_percentual: Optional[float] = 0.0
    criado_em: datetime

    class Config:
        from_attributes = True

class TotalFaturamento(BaseModel):
    total_anual: float
    media_mensal: float