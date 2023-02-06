from fastapi.testclient import TestClient

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
