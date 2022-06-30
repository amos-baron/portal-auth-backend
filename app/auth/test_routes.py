from fastapi.testclient import TestClient
from helpers import create_access_token
from app.main import app
from schemas import KeyCloakUser

client = TestClient(app)


def test_inspect_unauthorized():
    response = client.get("/auth/inspect")
    assert response.status_code == 200
    assert response.json() == {'validated': False}

def test_inspect_authorized():
    create_access_token(KeyCloakUser(name= "test ticles",sid="42069",email="123@coo.mer"))
    response = client.post(
        "/auth/inspect",
        cookies="",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {'validated': True}
