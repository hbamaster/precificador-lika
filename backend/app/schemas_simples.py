from pydantic import BaseModel
from typing import Optional

class SimplesNacionalReparticaoOut(BaseModel):
    irpj: float
    csll: float
    cofins: float
    pis: float
    cpp: float
    icms: float

class SimplesNacionalFaixaOut(BaseModel):
    id: int
    faturamento_inicio: float
    faturamento_fim: float
    aliquota: float
    deducao: float
    reparticao: Optional[SimplesNacionalReparticaoOut]

    class Config:
        from_attributes = True

class SimplesNacionalConsulta(BaseModel):
    faixa: SimplesNacionalFaixaOut
    aliquota_efetiva: float