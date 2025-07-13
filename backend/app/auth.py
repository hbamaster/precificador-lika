from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import Token
from .crud import get_user, verify_password
from .auth import create_access_token
from typing import Annotated
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Autenticação"])

@router.post(
    "/login",
    response_model=Token,
    summary="Autenticação de usuário",
    description="Realiza login e retorna token JWT",
    responses={
        401: {"description": "Credenciais inválidas"},
        500: {"description": "Erro interno no servidor"}
    }
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Autentica um usuário e retorna um token de acesso JWT.
    
    - **username**: Email ou nome de usuário
    - **password**: Senha do usuário
    """
    try:
        user = get_user(db, form_data.username)
        if not user or not verify_password(form_data.password, user.password_hash):
            logger.warning(f"Tentativa de login inválida para: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais incorretas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "access_token": create_access_token({"sub": user.username}),
            "token_type": "bearer",
            "expires_in": 3600
        }

    except Exception as e:
        logger.error(f"Erro durante login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro durante a autenticação"
        )