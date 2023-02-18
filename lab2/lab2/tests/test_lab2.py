from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "not implemented"}


def test_greeting_null_query():
    response = client.get("/hello/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Please provide a valid 'name' query parameter"
    }


def test_greeting():
    response = client.get("/hello?name=person")
    assert response.status_code == 200
    assert response.json() == "hello person"


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_json():
    response = client.get("/openapi.json")
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert datetime.fromisoformat(response.json()) 

def test_good_prediction_request():
    response = client.post(
        "/predict",
        headers={"accept": "application/json","Content-Type": "application/json"},
        json=[{"MedInc": 8.3252,"HouseAge": 41.0,"AveRooms": 6.98412698,"AveBedrms": 1.02380952,"Population": 322.0,"AveOccup": 2.55555556,"Latitude": 37.88,"Longitude": -122.23}]
    )
    assert response.status_code == 200

def test_bad_long_prediction_request():
    response = client.post(
        "/predict",
        headers={"accept": "application/json","Content-Type": "application/json"},
        json=[{"MedInc": 8.3252,"HouseAge": 41.0,"AveRooms": 6.98412698,"AveBedrms": 1.02380952,"Population": 322.0,"AveOccup": 2.55555556,"Latitude": 37.88,"Longitude": 202.23}]
    )
    assert response.status_code == 422
    assert response.json() ==  {'detail': [{'loc': ['body', 0, 'Longitude'], 'msg': 'not a valid longitude', 'type': 'value_error'}]}

def test_bad_lat_prediction_request():
    response = client.post(
        "/predict",
        headers={"accept": "application/json","Content-Type": "application/json"},
        json=[{"MedInc": 8.3252,"HouseAge": 41.0,"AveRooms": 6.98412698,"AveBedrms": 1.02380952,"Population": 322.0,"AveOccup": 2.55555556,"Latitude": 97.88,"Longitude": 122.23}]
    )
    assert response.status_code == 422
    assert response.json() ==  {'detail': [{'loc': ['body', 0, 'Latitude'], 'msg': 'not a valid latitude', 'type': 'value_error'}]}

def test_missing_prediction_request():
    response = client.post(
        "/predict",
        headers={"accept": "application/json","Content-Type": "application/json"},
        json=[{"HouseAge": 41.0,"AveRooms": 6.98412698,"AveBedrms": 1.02380952,"Population": 322.0,"AveOccup": 2.55555556,"Latitude": 37.88,"Longitude": 122.23}]
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 0, 'MedInc'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_multiple_good_prediction_request():
    response = client.post(
        "/predict",
        headers={"accept": "application/json","Content-Type": "application/json"},
        json=[
        {"MedInc": 8.3252,"HouseAge": 41.0,"AveRooms": 6.98412698,"AveBedrms": 1.02380952,"Population": 322.0,"AveOccup": 2.55555556,"Latitude": 37.88,"Longitude": -122.23},
        {"MedInc": 8.3252,"HouseAge": 41.0,"AveRooms": 6.98412698,"AveBedrms": 1.02380952,"Population": 322.0,"AveOccup": 2.55555556,"Latitude": 37.88,"Longitude": 122.23}]
    )
    assert response.status_code == 200