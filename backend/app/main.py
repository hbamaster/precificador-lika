from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from .database import engine, Base
from .routers import (
    auth, config_bling, config_operacional, 
    config_precificacao, faturamento, simples, 
    indicadores, frete
)
from .middleware import LoggingMiddleware
import os
from typing import List

app = FastAPI(
    title="API de Precificação",
    description="Backend para gestão de custos e fretes",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENV", "dev") == "dev" else None,
    redoc_url=None
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

# Metrics
Instrumentator().instrument(app).expose(app)

# Rotas
routers: List = [
    auth.router,
    config_bling.router,
    config_operacional.router,
    config_precificacao.router,
    faturamento.router,
    simples.router,
    indicadores.router,
    frete.router
]

for router in routers:
    app.include_router(router)

@app.on_event("startup")
async def startup():
    """Inicializa recursos na startup"""
    init_db()
    # Adicione outras inicializações aqui

@app.get("/health", include_in_schema=False)
async def health_check():
    """Endpoint de saúde da aplicação"""
    return {"status": "healthy", "database": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.on_event("startup")
def iniciar_fretes():
    db = next(get_db())
    refazer_fretes_mercadolivre(db)
    refazer_fretes_magalu(db)
    refazer_fretes_amazon(db)
    db.commit()