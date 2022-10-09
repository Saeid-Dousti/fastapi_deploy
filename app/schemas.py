# minute 5:33
# 8:35, add relational. to retrieve owner info from UserOut based on owner_id
# 10:24 changed to include join for vote count of each post and introduced PostOut class
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class UserCreate(
    BaseModel
):  # what a response post should look like, basically no extra fields like created_at or id should be returned!
    email: EmailStr #*
    password: str


class UserOut(
    BaseModel
):  #* what a response post should look like, basically no extra fields like created_at or id should be returned!
    id: int
    email: EmailStr #*
    created_at: datetime #*
    
    class Config:  # this makes sure the response back is not a sqlalchemy type object, but it is a dictionary
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel): # 7:14,
    access_token: str
    token_type: str

class TokenData(BaseModel): # 7:15, the user id that is used to create token, basically what comes out from decoding the token
    id: Optional[str] = None


class PostBase(BaseModel):  # what a post should look like
    title: str
    content: str
    published: bool = True


class PostCreate(
    PostBase
):  # inherits from PostBase to manage created posts, essentially same as PostBase
    pass # owner_id: int #* 8:08


# class Post(BaseModel): # what a response post should look like, basically no extra fields like created_at or id should be returned!
#     id: int
#     title: str
#     content: str
#     published: bool
#     created_at: datetime


class Post(
    PostBase
):  # what a response post should look like, basically no extra fields like created_at or id should be returned!
    id: int
    created_at: datetime
    owner_id: int # 8:15
    owner: UserOut #8:35 make sure UserOut class is defined before Post so it can be recognized

    class Config:  # this makes sure the response back is not a sqlalchemy type object, but it is a dictionary
        orm_mode = True


class PostOut(BaseModel): #* 10:24 join to include votes of each post
    Post: Post
    votes: int

    class Config:  # this makes sure the response back is not a sqlalchemy type object, but it is a dictionary
        orm_mode = True

class Vote(
    BaseModel
):
    dir: conint(le=1)
    post_id:int
