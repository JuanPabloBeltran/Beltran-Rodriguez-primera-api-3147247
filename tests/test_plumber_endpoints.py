# tests/test_plumber_endpoints.py
def test_create_reparacion_requires_auth(client):
    payload = {
        "cliente": "Juan Pérez",
        "direccion": "Cra 15 #45-23",
        "tipo_problema": "fuga_agua",
        "estado": "pendiente",
        "costo_estimado": 150000
    }
    r = client.post("/plumber/reparaciones/", json=payload)
    assert r.status_code == 401

def test_create_reparacion_success(client, auth_header):
    payload = {
        "cliente": "Juan Pérez",
        "direccion": "Cra 15 #45-23",
        "tipo_problema": "fuga_agua",
        "estado": "pendiente",
        "costo_estimado": 150000
    }
    r = client.post("/plumber/reparaciones/", json=payload, headers=auth_header)
    assert r.status_code == 201
    data = r.json()
    assert data["tipo_problema"] == "fuga_agua"
    assert "id" in data

def test_get_list_and_get_by_id(client, auth_header):
    # crear 2 reparaciones
    payload = {
        "cliente": "A",
        "direccion": "Dir A",
        "tipo_problema": "tuberia_rota",
        "estado": "pendiente",
        "costo_estimado": 50000
    }
    r1 = client.post("/plumber/reparaciones/", json=payload, headers=auth_header)
    r2 = client.post("/plumber/reparaciones/", json=payload, headers=auth_header)
    assert r1.status_code == 201 and r2.status_code == 201

    list_r = client.get("/plumber/reparaciones/")
    assert list_r.status_code == 200
    assert isinstance(list_r.json(), list)
    assert len(list_r.json()) >= 2

    first_id = list_r.json()[0]["id"]
    get_r = client.get(f"/plumber/reparaciones/{first_id}")
    assert get_r.status_code == 200
    assert get_r.json()["id"] == first_id

def test_update_and_delete(client, auth_header):
    payload = {
        "cliente": "B",
        "direccion": "Dir B",
        "tipo_problema": "grifos",
        "estado": "pendiente",
        "costo_estimado": 80000
    }
    create = client.post("/plumber/reparaciones/", json=payload, headers=auth_header)
    rid = create.json()["id"]

    update_payload = payload.copy()
    update_payload["estado"] = "completado"
    up = client.put(f"/plumber/reparaciones/{rid}", json=update_payload, headers=auth_header)
    assert up.status_code == 200
    assert up.json()["estado"] == "completado"

    del_r = client.delete(f"/plumber/reparaciones/{rid}", headers=auth_header)
    assert del_r.status_code == 204
    get_after = client.get(f"/plumber/reparaciones/{rid}")
    assert get_after.status_code == 404
