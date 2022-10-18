# 15:49

from http import client
from multiprocessing import AuthenticationError
from turtle import title
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app # to test it
# from app.config import settings
from app.database import get_db, Base
from alembic import command #* 15:43 use alembic to downgrade and upgrade tables
from app.oauth2 import create_access_token #* 16:30
from app import models


# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# we can hardcode this
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:password123@localhost:5432/fastapi_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)
# Base = declarative_base()

# Dependency
# def override_get_db(): #* 15:43
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

@pytest.fixture #* 16:01
def session():
    Base.metadata.drop_all(bind=engine) # drop tables
    Base.metadata.create_all(bind=engine) # create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture #* 16:01
def client(session): #* 15:46
    def override_get_db(): #* 15:43
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # run our code after our test finishes

@pytest.fixture
def test_user(client): #* 16:20
    user_data = {"email":"sanjeev@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data) # it is like request library
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client): #* 17:12 creating another user
    user_data = {"email":"sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data) # it is like request library
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture #* 16:32
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture #* 16:36, updated 17:13 by adding second user's post
def test_posts(session, test_user, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']  #* 17:13, this post will be tried to be deleted by test_user
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)

    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    return session.query(models.Post).all()
