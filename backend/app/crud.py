from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Busca usuário por nome
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Verifica se senha é válida
def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)

# Autentica usuário
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

# Cria usuário ADMIN caso não exista
def create_admin_if_not_exist(db: Session):
    if not get_user(db, "ADMIN"):
        hashed = pwd_ctx.hash("ADMIN")
        db.add(models.User(username="ADMIN", password_hash=hashed))
        db.commit()

# Busca configuração atual do Bling
def get_config(db: Session):
    return db.query(models.ConfigBling).first()

# Atualiza (ou cria) configuração do Bling
def update_config(db: Session, apikey_enc, versao_api):
    cfg = get_config(db)
    if not cfg:
        cfg = models.ConfigBling(apikey_encrypted=apikey_enc, versao_api=versao_api)
        db.add(cfg)
    else:
        cfg.apikey_encrypted = apikey_enc
        cfg.versao_api = versao_api
    db.commit()
    return cfg