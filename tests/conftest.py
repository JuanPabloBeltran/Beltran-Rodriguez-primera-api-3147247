# tests/conftest.py
import pytest
import sys, os
from fastapi.testclient import TestClient

# Asegurar que la carpeta raíz esté en sys.path (si es necesario)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_header():
    return {"X-API-KEY": "secret-plumber-key"}
