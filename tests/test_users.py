import pytest
from jose import jwt
from app import schemas
from app.config import settings
# from .database import client, session #* 16:20



# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World which is ok!!!'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password":"password123"})
    new_user = schemas.UserOut(**res.json())  #15:24 do some level of validation making sure everythign looks good
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user): #* 16:19
    res = client.post("/login", data={"username": test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
]) #* 16:25
def test_incorrect_login_user(client, test_user, email, password, status_code): #* 16:22
    #wrong password:
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'


