import pytest
from app import schemas
from .database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email":"sanjeev@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World which is ok!!!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password":"password123"})
    new_user = schemas.UserOut(**res.json())  #15:24 do some level of validation making sure everythign looks good
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user): #* 15:53
    res = client.post("/login", data={"username": "hello123@gmail.com", "password":"password123"})

    assert res.status_code == 200