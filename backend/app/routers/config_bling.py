# app/routers/config_bling.py  (ATUALIZADO)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, database, auth, schemas
from cryptography.fernet import Fernet
from datetime import datetime
import requests
from ..config import settings

router = APIRouter(prefix="/api/config/bling", tags=["Configuração"])

fernet = Fernet(settings.fernet_key.encode())

@router.get("", response_model=schemas.ConfigBlingOut)
def get_config(db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    cfg = crud.get_config(db)
    if not cfg:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    apikey = fernet.decrypt(cfg.apikey_encrypted.encode()).decode()
    return {
        "apikey": apikey[:4] + "****",
        "versao_api": cfg.versao_api,
        "ultimo_status": cfg.ultimo_status,
        "ultimo_teste_em": cfg.ultimo_teste_em,
        "ultimo_mensagem": cfg.ultimo_mensagem
    }

@router.post("", response_model=schemas.ConfigBlingOut)
def save_config(data: schemas.ConfigBlingIn, db: Session = Depends(database.get_db), user=Depends(auth.get_current_user)):
    encrypted = fernet.encrypt(data.apikey.encode()).decode()
    crud.update_config(db, encrypted, data.versao_api)
    return get_config(db)