from fastapi import FastAPI

from app.routers.optimized_routes import router as catalogo_router
from app.middleware.logging import logger
from monitoring.metrics import router as metrics_router
from monitoring.dashboard import router as dashboard_router

app = FastAPI()

# Integrar router de catálogo

app.include_router(catalogo_router)
app.include_router(metrics_router)
app.include_router(dashboard_router)

@app.get("/")
def read_root():
    return {"message": "API Optimizada Genérica - Tipo D"}

# Ejemplo de integración de logging (solo para mostrar logs en consola)
import logging
logging.basicConfig(level=logging.INFO)
logger.info("API Tipo D iniciada y lista para recibir requests")
