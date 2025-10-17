import os
import sys

# Asegurar que la raíz del repo esté en sys.path antes de importar src.app
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

# Setear JWT_SECRET_KEY antes de importar la app
os.environ["JWT_SECRET_KEY"] = "test_secret_local"

import pytest
from src.app import app
from config.database import engine, Base

@pytest.fixture(autouse=True)
def setup_db():
    # recrea las tablas para un estado limpio antes de cada test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_register_login_and_protected_flow(client):
    # Registrar usuario de prueba
    resp = client.post("/api/usuarios", json={
        "name": "testuser",
        "correo": "testuser@example.com",
        "password": "pass123"
    })
    assert resp.status_code in (200, 201)

    # Login válido -> obtener token
    resp = client.post("/api/login", json={
        "name": "testuser",
        "password": "pass123"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    token = data["access_token"]

    # Acceso a ruta protegida con token
    resp = client.get("/api/usuarios", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

def test_login_invalid_credentials(client):
    resp = client.post("/api/login", json={"name": "noexiste", "password": "x"})
    assert resp.status_code == 401

def test_protected_route_without_token(client):
    resp = client.get("/api/usuarios")
    assert resp.status_code in (401, 422)