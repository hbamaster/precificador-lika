from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, frete, indicadores  # exemplo
from app.dependencies import get_db

app = FastAPI()

# CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # dev local (Next.js)
        "https://precificador-site.onrender.com",  # futuro frontend Render
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router)
app.include_router(frete.router)
app.include_router(indicadores.router)