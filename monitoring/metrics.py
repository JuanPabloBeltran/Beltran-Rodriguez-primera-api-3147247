from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import APIRouter, Response

catalogo_requests = Counter('catalogo_requests_total', 'Total de requests a catálogo')
catalogo_search_duration = Histogram('catalogo_search_duration_seconds', 'Duración de búsquedas en catálogo')
inventario_precision = Gauge('inventario_precision', 'Precisión del inventario reportado')

router = APIRouter()

@router.get("/metrics")
def metrics():
	return Response(generate_latest(), media_type="text/plain")
# Métricas estándar de API
from prometheus_client import Counter, Histogram

request_counter = Counter('requests_total', 'Total de requests')
request_histogram = Histogram('request_duration_seconds', 'Duración de requests')
