from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, frete, indicadores  # Ajuste conforme seus módulos

app = FastAPI()

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router)
app.include_router(frete.router)
app.include_router(indicadores.router)

# Rota de status simples
@app.get("/health")
def health_check():
    return {"status": "ok"}