# tests/test_crud_frete.py
import pytest
from app.database import Base, engine, SessionLocal
from app.models_frete import FreteMercadoLivre
from app.crud_frete import buscar_valor_frete
from app.schemas_frete import FreteEntrada

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_buscar_ml(db):
    db.add(FreteMercadoLivre(
        modalidade="full",
        categoria="eletronicos",
        faixa_preco="0-100",
        peso_min=0.0, peso_max=5.0, valor_frete=10.0
    ))
    db.commit()
    info = FreteEntrada(
        marketplace="Mercado Livre",
        modalidade="full",
        peso=2.0,
        preco_produto=50.0,
        categoria="eletronicos"
    )
    valor = buscar_valor_frete(db, info)
    assert valor == 10.0