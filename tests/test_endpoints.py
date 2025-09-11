def test_create_reparacion_plomeria(client):
    data = {
        "cliente": "Juan Pérez",
        "direccion": "Cra 15 #45-23",
        "tipo_problema": "fuga_agua",
        "estado": "pendiente",
        "costo_estimado": 150000
    }
    headers = {"X-API-Key": "secret-plumber-key"}  # 👈 valor exacto del main.py
    response = client.post("/plumber/reparaciones/", json=data, headers=headers)
    assert response.status_code == 201
