from sqlalchemy.orm import Session
from . import models_precificacao as models
from . import schemas_precificacao as schemas

# Lista fixa de canais iniciais
CANAIS_PADRAO = [
    "Venda direta", "Site", "Mercado Livre", "Amazon",
    "Magazine Luiza", "Shopee", "Coopera", "Kabum",
    "FarmaDelivery", "ATACADO"
]

# ---------- Inicialização ----------
def inicializar_canais(db: Session):
    for nome in CANAIS_PADRAO:
        existente = db.query(models.MargemCanal).filter_by(canal=nome).first()
        if not existente:
            canal = models.MargemCanal(canal=nome, margem_desejada=0.0)
            db.add(canal)
    db.commit()

# ---------- Listagem ----------
def listar_canais(db: Session, incluir_inativos: bool = True):
    query = db.query(models.MargemCanal)
    if not incluir_inativos:
        query = query.filter_by(inativo=False)
    return query.order_by(models.MargemCanal.canal).all()

# ---------- Atualização ----------
def atualizar_canal(db: Session, id: int, dados: schemas.MargemCanalCreate):
    canal = db.query(models.MargemCanal).filter_by(id=id).first()
    if canal:
        for key, value in dados.dict().items():
            setattr(canal, key, value)
        db.commit()
        db.refresh(canal)
    return canal

# ---------- Exclusão ----------
def excluir_canal(db: Session, id: int):
    canal = db.query(models.MargemCanal).filter_by(id=id).first()
    if canal:
        db.delete(canal)
        db.commit()