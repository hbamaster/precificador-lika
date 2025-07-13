from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from .. import database
from ..schemas_frete import FreteEntrada, FreteSaida
from ..crud_frete import buscar_valor_frete
from ..auth import get_current_user

router = APIRouter(prefix="/api/fretes", tags=["Fretes"])

@router.post(
    "/calcular",
    response_model=FreteSaida,
    name="Calcular frete",
    description="Calcula o valor do frete para um produto com base no marketplace, peso, preço e categoria",
    responses={
        200: {"description": "Cálculo realizado com sucesso", "model": FreteSaida},
        404: {"description": "Regras de frete não encontradas para os parâmetros informados"},
        422: {"description": "Parâmetros inválidos", "content": {"application/json": {"example": {"detail": "Peso deve ser positivo"}}}}
    }
)
@cache(expire=3600)  # Cache de 1 hora
def calcular_frete(
    info: FreteEntrada,
    db: Session = Depends(database.get_db)
):
    """
    Calcula o frete para um produto com base em:
    - Marketplace (Mercado Livre, Amazon, etc.)
    - Modalidade (full, dba, etc.)
    - Peso do produto (em kg)
    - Preço do produto
    - Categoria (opcional)
    - Nível logístico (opcional)
    """
    try:
        valor = buscar_valor_frete(db, info)
        return FreteSaida(valor=valor)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/atualizar/{marketplace}",
    name="Atualizar tabela de fretes",
    description="Atualiza as regras de cálculo de frete para um marketplace específico via arquivo CSV",
    responses={
        200: {"description": "Tabela atualizada com sucesso", "content": {"application/json": {"example": {"status": "ok", "registros": 150}}}},
        400: {"description": "Formato de arquivo inválido"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado (requer perfil admin)"}
    }
)
async def atualizar_tabela_frete(
    marketplace: str,
    arquivo: UploadFile = File(..., description="Arquivo CSV com as novas regras de frete"),
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    """
    Atualiza a tabela de fretes para um marketplace específico.
    
    Requer:
    - Arquivo CSV formatado corretamente
    - Permissão de administrador
    """
    if not arquivo.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Formato inválido. Envie um arquivo CSV"
        )

    # TODO: Implementar lógica de parsing e atualização
    # 1. Validar estrutura do CSV
    # 2. Processar linhas
    # 3. Atualizar banco de dados
    
    return {
        "status": "ok",
        "registros": 150,  # Exemplo
        "marketplace": marketplace,
        "observacao": "Endpoint em implementação"
    }