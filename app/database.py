"""
    4:38:05
    https://fastapi.tiangolo.com/tutorial/sql-databases/
    this will be used in main_15 and onward
    also models.py
"""
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# before we were using psycopg2.connect, now we use url

# only for sqlite:
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'  <--- template (bad practice)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Samad!867@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

## only for sqlite
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                         password='Samad!867', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() # this is to execute SQL statements
#         print('Database connection was successfull!')
#         break

#     except Exception as error:
#         print('Connecting to database failed')
#         print('Error:', error)
#         time.sleep(2)