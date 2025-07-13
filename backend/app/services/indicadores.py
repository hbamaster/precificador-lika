# app/services/indicadores.py
from sqlalchemy.orm import Session
from ..crud_faturamento import total_faturamento
from ..crud_simp as crud_simples
from ..crud_operacional import calcular_totais
from ..crud_precificacao import listar_canais

def calcular_indicadores_tecnicos(db: Session):
    tot = total_faturamento(db)
    # ...
    return {...}

def calcular_indicadores_comerciais(db: Session):
    canais = listar_canais(db, incluir_inativos=False)
    # ...
    return {...}