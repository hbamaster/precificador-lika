from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud_faturamento as crud
from .. import schemas_faturamento as schemas
from .. import database, auth

router = APIRouter(prefix="/api/faturamento", tags=["Faturamento Observado"])

# 📅 Inserir ou atualizar mês
@router.post("", response_model=schemas.FaturamentoMensalOut, name="Salvar mês")
def salvar_mes(data: schemas.FaturamentoMensalCreate, db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    return crud.salvar_faturamento(db, data)

# 📋 Listar os 12 meses
@router.get("", response_model=list[schemas.FaturamentoMensalOut], name="Listar meses")
def listar_meses(db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    return crud.listar_faturamentos(db)

# 📊 Total e média anual
@router.get("/total", response_model=schemas.TotalFaturamento, name="Total anual de faturamento")
def total_anual(db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    return crud.total_faturamento(db)

# ❌ Remover mês
@router.delete("/{id}", name="Excluir mês")
def excluir_mes(id: int, db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    crud.excluir_faturamento(db, id)
    return {"status": "ok"}