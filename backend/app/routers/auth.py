from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth import login_for_access_token
from app.schemas import Token
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_for_access_token(form_data, db)