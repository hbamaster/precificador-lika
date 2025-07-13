import requests

BASE_URL = "http://localhost:8000/api"
AUTH_HEADER = {"Authorization": "Bearer <seu_token_jwt>"}

def criar_lancamento_operacional():
    print("🔹 Criando categoria 'Despesas Fixas'...")
    r1 = requests.post(f"{BASE_URL}/config/operacional/categorias", json={
        "nome": "Despesas Fixas", "tipo": "despesa", "ordem": 1
    }, headers=AUTH_HEADER)
    categoria_id = r1.json()["id"]

    print("🔹 Criando subcategoria 'Aluguel'...")
    r2 = requests.post(f"{BASE_URL}/config/operacional/subcategorias", json={
        "nome": "Aluguel", "categoria_id": categoria_id, "ordem": 1
    }, headers=AUTH_HEADER)
    sub_id = r2.json()["id"]

    print("🔹 Criando lançamento de R$ 2000,00...")
    r3 = requests.post(f"{BASE_URL}/config/operacional/lancamentos", json={
        "nome": "Aluguel sede", "valor_mensal": 2000.0, "subcategoria_id": sub_id
    }, headers=AUTH_HEADER)
    print("✅ Lançamento criado:", r3.json())

def inserir_faturamento():
    print("🔹 Inserindo 12 meses de faturamento...")
    meses = [
        ("Jan/25", 202501, 20503.71),
        ("Fev/25", 202502, 26049.94),
        ("Mar/25", 202503, 31497.55),
        ("Abr/25", 202504, 27520.07),
        ("Mai/25", 202505, 28578.10),
        ("Jun/25", 202506, 32958.29),
        ("Jul/25", 202507, 25622.53),
        ("Ago/24", 202408, 16611.65),
        ("Set/24", 202409, 26736.92),
        ("Out/24", 202410, 37324.36),
        ("Nov/24", 202411, 26241.91),
        ("Dez/24", 202412, 16725.37),
    ]
    for m, oc, val in meses:
        requests.post(f"{BASE_URL}/faturamento", json={
            "mes_referencia": m,
            "ordem_cronologica": oc,
            "faturamento": val
        }, headers=AUTH_HEADER)
    print("✅ Faturamento registrado.")

def consultar_indicadores():
    print("🔍 Consultando indicadores para precificação...")
    r = requests.get(f"{BASE_URL}/indicadores", headers=AUTH_HEADER)
    indicadores = r.json()
    for k, v in indicadores.items():
        print(f"{k}: {v}")

def executar_teste():
    criar_lancamento_operacional()
    inserir_faturamento()
    consultar_indicadores()

if __name__ == "__main__":
    executar_teste()