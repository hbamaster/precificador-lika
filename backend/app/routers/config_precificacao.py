from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud_precificacao as crud
from .. import schemas_precificacao as schemas
from .. import database, auth

router = APIRouter(prefix="/api/config/margens", tags=["Margem por Canal"])

# 🔧 Inicialização dos canais padrão
@router.post("/inicializar", name="Criar canais padrão")
def inicializar(db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    crud.inicializar_canais(db)
    return {"status": "canais criados"}

# 📋 Listar canais
@router.get("", response_model=list[schemas.MargemCanalOut], name="Listar canais")
def listar(incluir_inativos: bool = True, db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    return crud.listar_canais(db, incluir_inativos)

# 🛠 Atualizar canal
@router.put("/{id}", response_model=schemas.MargemCanalOut, name="Atualizar canal")
def atualizar(id: int, data: schemas.MargemCanalCreate, db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    canal = crud.atualizar_canal(db, id, data)
    if not canal:
        raise HTTPException(status_code=404, detail="Canal não encontrado")
    return canal

# ❌ Excluir canal
@router.delete("/{id}", name="Excluir canal")
def excluir(id: int, db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    crud.excluir_canal(db, id)
    return {"status": "ok"}