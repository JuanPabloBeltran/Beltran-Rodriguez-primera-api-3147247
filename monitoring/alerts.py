# Alertas automáticas para catálogo de elementos (Tipo D)
import logging

def check_alerts(catalogo_requests, inventario_precision):
    if catalogo_requests > 1000:
        logging.warning("ALERTA: Alto volumen de búsquedas en catálogo")
    if inventario_precision < 0.9:
        logging.warning("ALERTA: Precisión de inventario baja")
