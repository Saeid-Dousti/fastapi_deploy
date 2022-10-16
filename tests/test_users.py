from http import client
from fastapi.testclient import TestClient
from app.main import app # to test it
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World which is ok!!!'
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password":"password123"})
    new_user = schemas.UserOut(**res.json())  #15:24 do some level of validation making sure everythign looks good
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201