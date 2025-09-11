# tests/test_plumber_auth.py
def test_create_requires_valid_api_key(client):
    payload = {
        "cliente": "Auth",
        "direccion": "Auth Dir",
        "tipo_problema": "fuga_agua",
        "estado": "pendiente",
        "costo_estimado": 1000
    }
    # header incorrecto
    r = client.post("/plumber/reparaciones/", json=payload, headers={"X-API-KEY": "wrong"})
    assert r.status_code == 401
