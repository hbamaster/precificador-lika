from pydantic import BaseModel
from typing import Optional

# 🔹 Indicadores por canal
class IndicadoresOut(BaseModel):
    margem_observada: float
    margem_desejada: float
    margem_final: float

# 🔹 Indicadores técnicos (Simples + despesas + faturamento)
class IndicadoresTecnicosOut(BaseModel):
    faturamento_12_meses: float
    aliquota_sem_st: float
    aliquota_com_st: float
    percentual_despesas: Optional[float]