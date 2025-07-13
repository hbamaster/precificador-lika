import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

# Configuração do cliente de teste
client = TestClient(app)

# Fixture para o banco de dados de teste
@pytest.fixture(scope="module")
def test_db() -> Generator:
    """
    Fixture que cria um banco de dados temporário para os testes.
    """
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Testes parametrizados para o Mercado Livre
@pytest.mark.parametrize(
    "peso, preco, categoria, esperado",
    [
        (0.3, 50.00, "normal", 39.90),  # Faixa 0.0–0.3 kg
        (1.5, 110.00, "normal", 18.76), # Faixa 1.0–2.0 kg
        (5.5, 199.99, "normal", 53.90), # Faixa 5.0-9.0 kg
    ],
    ids=[
        "faixa_0.3kg_ate_R$79",
        "faixa_1.5kg_R$100-119",
        "faixa_5.5kg_R$150-199"
    ]
)
def test_frete_mercado_livre_full(peso: float, preco: float, categoria: str, esperado: float):
    """
    Testa cálculo de frete para diferentes faixas do Mercado Livre FULL.
    Verifica se os valores retornados estão dentro da margem de 1% de tolerância.
    """
    response = client.post(
        "/api/fretes/calcular",
        json={
            "marketplace": "mercadolivre",
            "modalidade": "full",
            "peso": peso,
            "preco_produto": preco,
            "categoria": categoria
        }
    )
    assert response.status_code == 200, "Status code deve ser 200"
    assert "valor" in response.json(), "Resposta deve conter campo 'valor'"
    assert response.json()["valor"] == pytest.approx(esperado, rel=0.01), f"Valor deve ser aproximado a {esperado}"

# Testes para categorias especiais
def test_frete_ml_animal():
    """Testa cálculo para categoria especial (alimentos para animais)"""
    response = client.post(
        "/api/fretes/calcular",
        json={
            "marketplace": "mercadolivre",
            "modalidade": "full",
            "peso": 2.5,
            "preco_produto": 199.90,
            "categoria": "animal"
        }
    )
    assert response.status_code == 200
    assert response.json()["valor"] == pytest.approx(12.50, rel=0.01)

# Testes para outros marketplaces
@pytest.mark.parametrize(
    "marketplace,modalidade,payload,esperado",
    [
        (
            "magalu",
            "full",
            {"peso": 2.5, "preco_produto": 99.00, "nivel_logistico": "1"},
            25.45
        ),
        (
            "amazon",
            "dba",
            {"peso": 3.5, "preco_produto": 110.00},
            22.75
        ),
    ],
    ids=["magalu_nivel_1", "amazon_dba"]
)
def test_fretes_outros_marketplaces(marketplace: str, modalidade: str, payload: dict, esperado: float):
    """Testa cálculo de frete para outros marketplaces"""
    payload.update({
        "marketplace": marketplace,
        "modalidade": modalidade
    })
    response = client.post("/api/fretes/calcular", json=payload)
    assert response.status_code == 200
    assert response.json()["valor"] == pytest.approx(esperado, rel=0.01)

# Testes de validação
@pytest.mark.parametrize(
    "payload,mensagem_erro",
    [
        (
            {"marketplace": "mercadolivre", "modalidade": "full", "peso": -1, "preco_produto": 100.0},
            "Peso deve ser positivo"
        ),
        (
            {"marketplace": "mercadolivre", "modalidade": "full", "peso": 1.5, "preco_produto": -50.0},
            "Preço deve ser positivo"
        ),
        (
            {"marketplace": "invalido", "modalidade": "full", "peso": 1.5, "preco_produto": 100.0},
            "Marketplace não suportado"
        ),
    ],
    ids=["peso_negativo", "preco_negativo", "marketplace_invalido"]
)
def test_validacao_frete(payload: dict, mensagem_erro: str):
    """Testa validação de parâmetros inválidos"""
    response = client.post("/api/fretes/calcular", json=payload)
    assert response.status_code == 422, "Deveria falhar com código 422"
    assert mensagem_erro.lower() in response.text.lower(), f"Mensagem de erro deve conter '{mensagem_erro}'"

# Teste com banco de dados
def test_calculo_frete_com_db(test_db):
    """Testa integração com banco de dados"""
    payload = {
        "marketplace": "mercadolivre",
        "modalidade": "full",
        "peso": 1.5,
        "preco_produto": 150.0,
        "categoria": "normal"
    }
    response = client.post("/api/fretes/calcular", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json()["valor"], float)