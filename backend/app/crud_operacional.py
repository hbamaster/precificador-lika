from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models_operacional as models
from . import schemas_operacional as schemas

# ---------- Categoria ----------
def criar_categoria(db: Session, dados: schemas.CategoriaCustoCreate):
    cat = models.CategoriaCusto(**dados.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def listar_categorias(db: Session):
    return db.query(models.CategoriaCusto).order_by(models.CategoriaCusto.ordem).all()

def editar_categoria(db: Session, id: int, dados: schemas.CategoriaCustoCreate):
    cat = db.query(models.CategoriaCusto).filter_by(id=id).first()
    if cat:
        for key, value in dados.dict().items():
            setattr(cat, key, value)
        db.commit()
        db.refresh(cat)
    return cat

def excluir_categoria(db: Session, id: int):
    cat = db.query(models.CategoriaCusto).filter_by(id=id).first()
    if cat:
        db.delete(cat)
        db.commit()

# ---------- Subcategoria ----------
def criar_subcategoria(db: Session, dados: schemas.SubcategoriaCustoCreate):
    sub = models.SubcategoriaCusto(**dados.dict())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

def listar_subcategorias(db: Session, categoria_id: int):
    return db.query(models.SubcategoriaCusto).filter_by(categoria_id=categoria_id).order_by(models.SubcategoriaCusto.ordem).all()

def editar_subcategoria(db: Session, id: int, dados: schemas.SubcategoriaCustoCreate):
    sub = db.query(models.SubcategoriaCusto).filter_by(id=id).first()
    if sub:
        for key, value in dados.dict().items():
            setattr(sub, key, value)
        db.commit()
        db.refresh(sub)
    return sub

def excluir_subcategoria(db: Session, id: int):
    sub = db.query(models.SubcategoriaCusto).filter_by(id=id).first()
    if sub:
        db.delete(sub)
        db.commit()

# ---------- Lançamento ----------
def criar_lancamento(db: Session, dados: schemas.LancamentoCustoCreate):
    lan = models.LancamentoCusto(**dados.dict())
    db.add(lan)
    db.commit()
    db.refresh(lan)
    return lan

def listar_lancamentos(db: Session, subcategoria_id: int):
    return db.query(models.LancamentoCusto).filter_by(subcategoria_id=subcategoria_id).all()

def editar_lancamento(db: Session, id: int, dados: schemas.LancamentoCustoCreate):
    lan = db.query(models.LancamentoCusto).filter_by(id=id).first()
    if lan:
        for key, value in dados.dict().items():
            setattr(lan, key, value)
        db.commit()
        db.refresh(lan)
    return lan

def excluir_lancamento(db: Session, id: int):
    lan = db.query(models.LancamentoCusto).filter_by(id=id).first()
    if lan:
        db.delete(lan)
        db.commit()

# ---------- Totalizadores ----------
def calcular_totais(db: Session):
    total_despesas = db.query(func.sum(models.LancamentoCusto.valor_mensal))\
        .join(models.SubcategoriaCusto).join(models.CategoriaCusto)\
        .filter(models.CategoriaCusto.tipo == "despesa").scalar() or 0.0

    total_investimentos = db.query(func.sum(models.LancamentoCusto.valor_mensal))\
        .join(models.SubcategoriaCusto).join(models.CategoriaCusto)\
        .filter(models.CategoriaCusto.tipo == "investimento").scalar() or 0.0

    return schemas.TotaisOperacionais(
        total_despesas=round(total_despesas, 2),
        total_investimentos=round(total_investimentos, 2),
        total_geral=round(total_despesas + total_investimentos, 2)
    )