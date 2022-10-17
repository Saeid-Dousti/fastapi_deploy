from app import schemas
from .database import client, session

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

def test_login_user(client): #* 15:53
    res = client.post("/login", data={"username": "hello123@gmail.com", "password":"password123"})

    assert res.status_code == 200