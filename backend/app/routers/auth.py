from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import crud, auth, database, schemas

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

@router.post("/login", response_model=schemas.Token, name="Autenticar usuário")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    crud.create_admin_if_not_exist(db)
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos")

    token = auth.create_access_token({"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600
    }

@router.post("/logout", name="Encerrar sessão (simulado)")
def logout():
    return {"status": "ok"}