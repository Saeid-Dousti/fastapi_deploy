# 15:49

from http import client
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app # to test it
# from app.config import settings
from app.database import get_db, Base
from alembic import command #* 15:43 use alembic to downgrade and upgrade tables


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

@pytest.fixture(scope="module") #* 16:01
def session():
    Base.metadata.drop_all(bind=engine) # drop tables
    Base.metadata.create_all(bind=engine) # create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module") #* 16:01
def client(session): #* 15:46
    def override_get_db(): #* 15:43
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # run our code after our test finishes
