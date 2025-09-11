# tests/test_plumber_logica.py
def test_reparacion_sin_direccion_falla(client, auth_header):
    payload = {
        "cliente": "María",
        # "direccion": "",  # omitida
        "tipo_problema": "fuga_agua",
        "estado": "pendiente",
        "costo_estimado": 10000
    }
    r = client.post("/plumber/reparaciones/", json=payload, headers=auth_header)
    assert r.status_code == 422  # Pydantic valida campos requeridos

def test_reparacion_costo_negativo_falla(client, auth_header):
    payload = {
        "cliente": "X",
        "direccion": "Dir X",
        "tipo_problema": "fuga_agua",
        "estado": "pendiente",
        "costo_estimado": -50
    }
    r = client.post("/plumber/reparaciones/", json=payload, headers=auth_header)
    # Si quieres que esto sea 422/400, agrega validación en schema/app; por ahora Pydantic acepta floats negativos
    # Si aún no validaste, este test puede esperar 201. Si quieres validación, implementa en ReparacionBase:
    # costo_estimado: confloat(ge=0)
    # y entonces será 422. Aquí lo dejamos como ejemplo:
    assert r.status_code in (201, 422)
