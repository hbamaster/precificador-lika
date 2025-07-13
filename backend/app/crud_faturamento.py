from sqlalchemy.orm import Session
from . import models_faturamento as models
from . import schemas_faturamento as schemas
from sqlalchemy import func

# ----------- Inserção ou Atualização -----------

def salvar_faturamento(db: Session, dados: schemas.FaturamentoMensalCreate):
    existente = db.query(models.FaturamentoMensal).filter_by(ordem_cronologica=dados.ordem_cronologica).first()

    if existente:
        for key, value in dados.dict().items():
            setattr(existente, key, value)
    else:
        novo = models.FaturamentoMensal(**dados.dict())
        db.add(novo)
        db.commit()
        existente = novo

    db.commit()
    db.refresh(existente)

    # Recalcular evolução percentual após qualquer alteração
    recalcular_evolucao(db)
    return existente

# ----------- Listagem -----------

def listar_faturamentos(db: Session):
    return db.query(models.FaturamentoMensal).order_by(models.FaturamentoMensal.ordem_cronologica).all()

# ----------- Recalcular evolução percentual -----------

def recalcular_evolucao(db: Session):
    todos = listar_faturamentos(db)
    anterior = None

    for atual in todos:
        if anterior:
            delta = atual.faturamento - anterior.faturamento
            evolucao = (delta / anterior.faturamento * 100) if anterior.faturamento else 0
            atual.evolucao_percentual = round(evolucao, 2)
        else:
            atual.evolucao_percentual = 0.0
        anterior = atual

    db.commit()

# ----------- Totalizador -----------

def total_faturamento(db: Session):
    lista = listar_faturamentos(db)
    total = sum([item.faturamento for item in lista])
    media = total / 12 if len(lista) == 12 else 0.0

    return schemas.TotalFaturamento(
        total_anual=round(total, 2),
        media_mensal=round(media, 2)
    )

# ----------- Exclusão (opcional, restrita) -----------

def excluir_faturamento(db: Session, id: int):
    reg = db.query(models.FaturamentoMensal).filter_by(id=id).first()
    if reg:
        db.delete(reg)
        db.commit()
        recalcular_evolucao(db)