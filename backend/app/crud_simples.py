import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models_simples as models
from . import schemas_simples as schemas

# ---------- Consulta por faturamento ----------
def consultar_faixa(db: Session, faturamento_12_meses: float) -> schemas.SimplesNacionalConsulta:
    faixa = db.query(models.SimplesNacionalFaixa)\
        .filter(models.SimplesNacionalFaixa.faturamento_inicio <= faturamento_12_meses)\
        .filter(models.SimplesNacionalFaixa.faturamento_fim >= faturamento_12_meses)\
        .first()

    if not faixa:
        logging.warning(f"Faturamento {faturamento_12_meses} fora das faixas do Simples Nacional")
        raise HTTPException(status_code=404, detail="Faturamento fora das faixas definidas")

    base = faturamento_12_meses
    calculo = ((base * faixa.aliquota / 100) - faixa.deducao) / base
    efetiva = round(calculo * 100, 4)

    logging.info(f"Faixa {faixa.id} encontrada. Alíquota efetiva: {efetiva}%")
    return schemas.SimplesNacionalConsulta(
        faixa=faixa,
        aliquota_efetiva=efetiva
    )

# ---------- Consulta de todas as faixas ----------
def listar_faixas(db: Session):
    logging.info("Listando todas as faixas do Simples Nacional")
    return db.query(models.SimplesNacionalFaixa)\
        .order_by(models.SimplesNacionalFaixa.id)\
        .all()

# ---------- Recriar tabela (uso interno dos desenvolvedores) ----------
def refazer_tabelas_simples(db: Session):
    # ⚠️ Esta função não deve ser exposta publicamente
    logging.warning("Recriando faixas e repartições do Simples Nacional")

    # Remove tudo
    db.query(models.SimplesNacionalReparticao).delete()
    db.query(models.SimplesNacionalFaixa).delete()

    # Faixas padrão