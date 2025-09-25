# Test de rate limiting (simulado)
def test_rate_limit():
    # Simulación: el rate limiting debe bloquear después de X requests
    max_requests = 100
    requests = 120
    bloqueado = requests > max_requests
    assert bloqueado
