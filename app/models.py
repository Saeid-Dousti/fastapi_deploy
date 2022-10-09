"""
    8:07:35
    https://fastapi.tiangolo.com/tutorial/sql-databases/
    this will be used in main_33 and onward
    and also database.py
"""

import email
from enum import unique

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey #
from sqlalchemy.orm import relationship # 8:35
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "posts"  # <---- name of the table

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")  
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )  
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),  nullable=False) #* 8:08

    owner = relationship("User") # 8:35, fetchs the user based on the owner_id for us, "User" is the model class name of the table, further modifications are needed in schemas.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    phone_number = Column(String) #* 11:13 to show case the auto generate feature of alembic

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    