from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud_simples as crud
from .. import schemas_simples as schemas
from .. import database, auth

router = APIRouter(prefix="/api/simples", tags=["Simples Nacional"])

@router.get(
    "/consulta",
    response_model=schemas.SimplesNacionalConsulta,
    name="Consultar faixa por faturamento",
    description="Consulta a faixa do Simples Nacional correspondente ao faturamento informado",
    responses={
        200: {"description": "Consulta realizada com sucesso"},
        400: {
            "description": "Faturamento inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Faturamento não pode ser negativo"}
                }
            }
        },
        401: {"description": "Não autorizado"},
        404: {
            "description": "Faixa não encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Faturamento fora das faixas definidas"}
                }
            }
        }
    }
)
def consultar_faixa(
    faturamento: float = Query(..., description="Faturamento dos últimos 12 meses", gt=0),
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    """
    Retorna a faixa do Simples Nacional e alíquotas correspondentes ao faturamento informado.
    
    Parâmetros:
    - faturamento: Valor decimal positivo dos últimos 12 meses
    """
    try:
        return crud.consultar_faixa(db, faturamento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/faixas",
    response_model=list[schemas.SimplesNacionalFaixaOut],
    name="Listar faixas do Simples",
    description="Lista todas as faixas de faturamento e alíquotas do Simples Nacional",
    responses={
        200: {"description": "Lista de faixas retornada com sucesso"},
        401: {"description": "Não autorizado"}
    }
)
def listar_faixas(
    db: Session = Depends(database.get_db),
    user=Depends(auth.get_current_user)
):
    """
    Retorna todas as faixas de faturamento cadastradas no sistema com suas respectivas
    alíquotas e repartições tributárias.
    """
    return crud.listar_faixas(db)