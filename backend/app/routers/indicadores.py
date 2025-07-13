import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, auth
from .. import crud_faturamento, crud_operacional, crud_simples
from .. import crud_precificacao
from ..schemas_indicadores import IndicadoresOut, IndicadoresTecnicosOut
from .. import calculadora_indicadores

router = APIRouter(prefix="/api/indicadores", tags=["Indicadores de Precificação"])

# 🔍 Indicadores técnicos: faturamento, Simples, despesas
@router.get("", response_model=IndicadoresTecnicosOut, name="Indicadores técnicos gerais")
def indicadores_gerais(
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    faturamento_info = crud_faturamento.total_faturamento(db)
    faturamento_total = faturamento_info.total_anual
    faturamento_medio = faturamento_info.media_mensal

    try:
        consulta_simples = crud_simples.consultar_faixa(db, faturamento_total)
    except HTTPException:
        logging.warning("Faturamento fora das faixas do Simples Nacional")
        raise HTTPException(status_code=400, detail="Faturamento fora das faixas do Simples Nacional")

    aliquota_sem_st = consulta_simples.aliquota_efetiva
    faixa_icms = consulta_simples.faixa.reparticao.icms or 0
    aliquota_com_st = round((consulta_simples.faixa.aliquota * faixa_icms) / 100, 4)

    totais_operacionais = crud_operacional.calcular_totais(db)
    custo_operacional = totais_operacionais.total_geral
    despesas_percentual = round((custo_operacional / faturamento_medio) * 100, 2) if faturamento_medio else 0.0

    return IndicadoresTecnicosOut(
        faturamento_12_meses=faturamento_total,
        aliquota_sem_st=aliquota_sem_st,
        aliquota_com_st=aliquota_com_st,
        percentual_despesas=despesas_percentual
    )

# 📊 Indicadores comerciais por canal
@router.get("/margem", response_model=IndicadoresOut, name="Indicadores por canal")
def indicadores_por_canal(db: Session = Depends(database.get_db)):
    canais = crud_precificacao.listar_canais(db, incluir_inativos=False)

    if not canais:
        logging.warning("Nenhum canal ativo encontrado para cálculo de margem")
        raise HTTPException(status_code=404, detail="Nenhum canal ativo encontrado.")

    margem_desejada = sum([c.margem_desejada for c in canais]) / len(canais)
    margem_observada = calculadora_indicadores.calcular_margem_observada()
    margem_final = round(margem_observada - margem_desejada, 2)

    logging.info(f"Margem desejada: {margem_desejada}%, observada: {margem_observada}%")
    return IndicadoresOut(
        margem_observada=margem_observada,
        margem_desejada=round(margem_desejada, 2),
        margem_final=margem_final
    )