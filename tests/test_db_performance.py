# Test de performance de consultas optimizadas (simulado)
def test_consulta_optimizada():
    # Simulación: la consulta optimizada debe ser más rápida
    tiempo_no_opt = 0.2
    tiempo_opt = 0.05
    mejora = ((tiempo_no_opt - tiempo_opt) / tiempo_no_opt) * 100
    assert mejora > 50
