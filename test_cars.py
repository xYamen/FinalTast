import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlalchemy import Connection
from app import app, get_db

# Assuming 'app' is your FastAPI app and you've defined the 'cars_table' elsewhere
client = TestClient(app)

# Mock the database dependency
@pytest.fixture
def mock_db():
    db_mock = MagicMock(Connection)
    app.dependency_overrides[get_db] = lambda: db_mock
    yield db_mock
    app.dependency_overrides.clear()

# Test for GET /cars/ with all cars
def test_get_all_cars(mock_db):
    mock_db.execute().mappings().fetchall.return_value = [
        {'id': 1, 'name': 'Toyota', 'model': 'Camry', 'year': 2021, 'price': 25000},
        {'id': 2, 'name': 'Honda', 'model': 'Accord', 'year': 2020, 'price': 24000},
    ]

    response = client.get("/cars/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['name'] == 'Toyota'

# Test for GET /cars/ with ID
def test_get_car_by_id(mock_db):
    mock_db.execute().mappings().first.return_value = {
        'id': 1, 'name': 'Toyota', 'model': 'Camry', 'year': 2021, 'price': 25000
    }

    response = client.get("/cars/", params={"id": 1})
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'Toyota'

# Test for POST /cars/
def test_create_car(mock_db):
    mock_db.execute().mappings().first.return_value = {
        'id': 1, 'name': 'Toyota', 'model': 'Camry', 'year': 2021, 'price': 25000
    }

    car_data = {"name": "Toyota", "model": "Camry", "year": 2021, "price": 25000}
    response = client.post("/cars/", json=car_data)

    assert response.status_code == 201
    assert response.json()['name'] == "Toyota"

# Test for PUT /cars/{car_id}
def test_update_car(mock_db):
    mock_db.execute().mappings().first.side_effect = [
        {'id': 1, 'name': 'Toyota', 'model': 'Camry', 'year': 2021, 'price': 25000},  # car exists check
        {'id': 1, 'name': 'Toyota', 'model': 'Camry', 'year': 2021, 'price': 26000},  # updated car
    ]

    car_data = {"name": "Toyota", "model": "Camry", "year": 2021, "price": 26000}
    response = client.put("/cars/1", json=car_data)

    assert response.status_code == 200
    assert response.json()['price'] == 26000

# Test for DELETE /cars/{car_id}
def test_delete_car(mock_db):
    mock_db.execute().mappings().first.return_value = {
        'id': 1, 'name': 'Toyota', 'model': 'Camry', 'year': 2021, 'price': 25000
    }

    response = client.delete("/cars/1")
    assert response.status_code == 204
