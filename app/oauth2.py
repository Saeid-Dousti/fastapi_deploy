# 7:14 with aut_31.py
# creates token and verifies
# 9:19

from fastapi import Depends, HTTPException, Response, status
from jose import JWSError, jwe
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import models #* 7:40
from . import schemas #* 7:18
from . import database #* 7:38
from fastapi.security import OAuth2PasswordBearer
from .config import settings

import jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login') # 7:21, tokenUrl: the endpoint of login url, the url is grabbed from auth.py


#SECRET_KEY
#Algorithm
#Expiration time

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict): #* which is the payload data data={"user_id":user.id}, you can add more things like role, etc.

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM]) # in mac you should put list
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt # this goes back to login path


def verify_access_token(token:str, credentials_exception): # 7:19

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) # verify the token_data here, basically user_id

    except JWSError: 
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)): 
    #* 7:38, we are gonna pass this as a dependency to path operations, and it'll take the token, get the id, 
    # verify that it is correct, fetch the user_id, and add it as a paramenter into path operation function
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user