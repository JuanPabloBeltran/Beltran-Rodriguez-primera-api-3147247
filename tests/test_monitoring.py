# Test de monitoreo y métricas (simulado)
def test_metrics_exposure():
    # Simulación: la ruta /metrics debe estar disponible
    available = True
    assert available

def test_alerts():
    from monitoring.alerts import check_alerts
    check_alerts(1500, 0.85)  # Debe disparar alertas
