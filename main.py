import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app import models
from app.database import engine
from app.routers import libros, auth

# 1. Inicializar la app de FastAPI UNA SOLA VEZ
app = FastAPI(title="API de la biblioteca con FastAPI y PostgreSQL")

# 2. Configurar CORS en esta única instancia
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# 4. Middleware para registrar el tiempo de respuesta de cada petición
@app.middleware("http")
async def agregar_tiempo_de_proceso(request: Request, call_next):
    inicio = time.time()
    response = await call_next(request)
    tiempo_total = time.time() - inicio
    response.headers["X-Process-Time"] = f"{tiempo_total:.4f}s"
    return response

@app.exception_handler(Exception)
async def manejador_errores_globales(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"mensaje": "Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde."}
    )

# 5. Incluir los routers
app.include_router(auth.router)
app.include_router(libros.router)