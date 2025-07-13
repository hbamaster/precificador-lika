# app/crud_frete.py
from sqlalchemy.orm import Session
from .models_frete import FreteMercadoLivre, FreteMagalu, FreteAmazon
from .schemas_frete import FreteEntrada
import csv
from io import StringIO

def _buscar_ml(db: Session, info: FreteEntrada) -> float:
    faixa = db.query(FreteMercadoLivre)\
        .filter_by(
            modalidade=info.modalidade,
            categoria=info.categoria,
            faixa_preco=info.faixa_preco
        )\
        .filter(FreteMercadoLivre.peso_min <= info.peso, FreteMercadoLivre.peso_max >= info.peso)\
        .first()
    if not faixa:
        raise ValueError("Regra MercadoLivre não encontrada")
    return faixa.valor_frete

def _buscar_magalu(db: Session, info: FreteEntrada) -> float:
    faixa = db.query(FreteMagalu)\
        .filter_by(nivel_logistico=info.nivel_logistico)\
        .filter(FreteMagalu.peso_min <= info.peso, FreteMagalu.peso_max >= info.peso)\
        .first()
    if not faixa:
        raise ValueError("Regra Magalu não encontrada")
    return faixa.valor_frete

def _buscar_amazon(db: Session, info: FreteEntrada) -> float:
    faixa = db.query(FreteAmazon)\
        .filter_by(modalidade=info.modalidade, faixa_preco=info.faixa_preco)\
        .filter(FreteAmazon.peso_min <= info.peso, FreteAmazon.peso_max >= info.peso)\
        .first()
    if not faixa:
        raise ValueError("Regra Amazon não encontrada")
    return faixa.valor_frete

def buscar_valor_frete(db: Session, info: FreteEntrada) -> float:
    mkt = info.marketplace.lower()
    if "mercado livre" in mkt:
        return _buscar_ml(db, info)
    if "magalu" in mkt:
        return _buscar_magalu(db, info)
    if "amazon" in mkt:
        return _buscar_amazon(db, info)
    raise ValueError("Marketplace não suportado")

def atualizar_tabela(db: Session, marketplace: str, csv_bytes: bytes) -> int:
    text = csv_bytes.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
    count = 0
    # Limpa tabela antes?
    # db.query(FreteMercadoLivre).delete()  # conforme necessidade
    for row in reader:
        # Exemplo para MercadoLivre
        if marketplace.lower() == "mercado livre":
            obj = FreteMercadoLivre(
                modalidade=row["modalidade"],
                categoria=row["categoria"],
                faixa_preco=row["faixa_preco"],
                peso_min=float(row["peso_min"]),
                peso_max=float(row["peso_max"]),
                valor_frete=float(row["valor_frete"])
            )
        # similar para Magalu/Amazon...
        db.merge(obj)
        count += 1
    db.commit()
    return count