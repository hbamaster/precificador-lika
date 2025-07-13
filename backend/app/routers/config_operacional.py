from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud_operacional as crud
from .. import schemas_operacional as schemas
from .. import database, auth
from .. import models_operacional as models  # Importação necessária para a paginação

router = APIRouter(prefix="/api/config/operacional", tags=["Custo Operacional"])

# Categorias
@router.get(
    "/categorias",
    response_model=list[schemas.CategoriaCustoOut],
    name="Listar categorias",
    description="Lista todas as categorias de custo com paginação"
)
def listar_categorias(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(100, le=500, description="Itens por página"),
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    offset = (page - 1) * limit
    return db.query(models.CategoriaCusto).offset(offset).limit(limit).all()

@router.post(
    "/categorias",
    response_model=schemas.CategoriaCustoOut,
    name="Criar categoria",
    responses={
        400: {"description": "Dados inválidos"},
        401: {"description": "Não autorizado"}
    }
)
def criar_categoria(
    data: schemas.CategoriaCustoCreate,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    return crud.criar_categoria(db, data)

@router.put(
    "/categorias/{id}",
    response_model=schemas.CategoriaCustoOut,
    name="Editar categoria",
    responses={
        404: {"description": "Categoria não encontrada"}
    }
)
def editar_categoria(
    id: int,
    data: schemas.CategoriaCustoCreate,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    cat = crud.editar_categoria(db, id, data)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return cat

@router.delete(
    "/categorias/{id}",
    name="Excluir categoria",
    responses={
        204: {"description": "Categoria excluída com sucesso"},
        404: {"description": "Categoria não encontrada"}
    }
)
def excluir_categoria(
    id: int,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    crud.excluir_categoria(db, id)
    return {"status": "ok"}

# Subcategorias
@router.get(
    "/subcategorias/{categoria_id}",
    response_model=list[schemas.SubcategoriaCustoOut],
    name="Listar subcategorias"
)
def listar_subcategorias(
    categoria_id: int,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    return crud.listar_subcategorias(db, categoria_id)

@router.post(
    "/subcategorias",
    response_model=schemas.SubcategoriaCustoOut,
    name="Criar subcategoria"
)
def criar_subcategoria(
    data: schemas.SubcategoriaCustoCreate,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    return crud.criar_subcategoria(db, data)

@router.put(
    "/subcategorias/{id}",
    response_model=schemas.SubcategoriaCustoOut,
    name="Editar subcategoria",
    responses={
        404: {"description": "Subcategoria não encontrada"}
    }
)
def editar_subcategoria(
    id: int,
    data: schemas.SubcategoriaCustoCreate,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    sub = crud.editar_subcategoria(db, id, data)
    if not sub:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    return sub

@router.delete(
    "/subcategorias/{id}",
    name="Excluir subcategoria",
    responses={
        204: {"description": "Subcategoria excluída com sucesso"}
    }
)
def excluir_subcategoria(
    id: int,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    crud.excluir_subcategoria(db, id)
    return {"status": "ok"}

# Lançamentos
@router.get(
    "/lancamentos/{subcategoria_id}",
    response_model=list[schemas.LancamentoCustoOut],
    name="Listar lançamentos"
)
def listar_lancamentos(
    subcategoria_id: int,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    return crud.listar_lancamentos(db, subcategoria_id)

@router.post(
    "/lancamentos",
    response_model=schemas.LancamentoCustoOut,
    name="Criar lançamento"
)
def criar_lancamento(
    data: schemas.LancamentoCustoCreate,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    return crud.criar_lancamento(db, data)

@router.put(
    "/lancamentos/{id}",
    response_model=schemas.LancamentoCustoOut,
    name="Editar lançamento",
    responses={
        404: {"description": "Lançamento não encontrado"}
    }
)
def editar_lancamento(
    id: int,
    data: schemas.LancamentoCustoCreate,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    lan = crud.editar_lancamento(db, id, data)
    if not lan:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    return lan

@router.delete(
    "/lancamentos/{id}",
    name="Excluir lançamento",
    responses={
        204: {"description": "Lançamento excluído com sucesso"}
    }
)
def excluir_lancamento(
    id: int,
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    crud.excluir_lancamento(db, id)
    return {"status": "ok"}

# Totais
@router.get(
    "/total",
    response_model=schemas.TotaisOperacionais,
    name="Calcular totais operacionais"
)
def calcular_totais(
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    return crud.calcular_totais(db)