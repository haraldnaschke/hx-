import importlib
import sys
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reset_store():
    """Reset the in-memory store before each test."""
    for mod in ["store", "main"]:
        if mod in sys.modules:
            del sys.modules[mod]
    yield


@pytest.fixture
def client(reset_store):
    import store  # noqa: F401 — fresh module
    from main import app
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_ferraris_returns_seeded_data(client):
    r = client.get("/ferraris")
    assert r.status_code == 200
    cars = r.json()
    assert len(cars) == 4
    models = {c["model"] for c in cars}
    assert "SF90 Stradale" in models


def test_get_ferrari(client):
    r = client.get("/ferraris/1")
    assert r.status_code == 200
    car = r.json()
    assert car["id"] == 1
    assert car["model"] == "SF90 Stradale"


def test_get_ferrari_not_found(client):
    r = client.get("/ferraris/999")
    assert r.status_code == 404


def test_create_ferrari(client):
    payload = {
        "model": "LaFerrari",
        "year": 2015,
        "engine": "Hybrid",
        "horsepower": 950,
        "top_speed_kmh": 350,
        "price_usd": 1400000,
    }
    r = client.post("/ferraris", json=payload)
    assert r.status_code == 201
    car = r.json()
    assert car["id"] is not None
    assert car["model"] == "LaFerrari"


def test_update_ferrari(client):
    r = client.patch("/ferraris/1", json={"horsepower": 1000})
    assert r.status_code == 200
    assert r.json()["horsepower"] == 1000


def test_update_ferrari_not_found(client):
    r = client.patch("/ferraris/999", json={"horsepower": 800})
    assert r.status_code == 404


def test_delete_ferrari(client):
    r = client.delete("/ferraris/1")
    assert r.status_code == 204
    r = client.get("/ferraris/1")
    assert r.status_code == 404


def test_delete_ferrari_not_found(client):
    r = client.delete("/ferraris/999")
    assert r.status_code == 404


def test_filter_by_year(client):
    r = client.get("/ferraris?year=2023")
    assert r.status_code == 200
    cars = r.json()
    assert all(c["year"] == 2023 for c in cars)


def test_filter_by_engine(client):
    r = client.get("/ferraris?engine=Hybrid")
    assert r.status_code == 200
    cars = r.json()
    assert all(c["engine"] == "Hybrid" for c in cars)


def test_create_validates_year(client):
    payload = {
        "model": "Test",
        "year": 1900,
        "engine": "V8",
        "horsepower": 500,
        "top_speed_kmh": 300,
        "price_usd": 100000,
    }
    r = client.post("/ferraris", json=payload)
    assert r.status_code == 422


def test_create_validates_horsepower(client):
    payload = {
        "model": "Test",
        "year": 2020,
        "engine": "V8",
        "horsepower": -1,
        "top_speed_kmh": 300,
        "price_usd": 100000,
    }
    r = client.post("/ferraris", json=payload)
    assert r.status_code == 422
