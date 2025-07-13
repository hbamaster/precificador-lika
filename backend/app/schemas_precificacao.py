from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MargemCanalBase(BaseModel):
    canal: str
    margem_desejada: Optional[float] = 0.0
    inativo: Optional[bool] = False

class MargemCanalCreate(MargemCanalBase):
    pass

class MargemCanalOut(MargemCanalBase):
    id: int
    margem_observada: float
    atualizado_em: datetime

    class Config:
        from_attributes = True	