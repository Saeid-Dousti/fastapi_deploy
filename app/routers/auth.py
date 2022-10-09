# 7:14 adding Token schema in schema.py

from fastapi.security.oauth2 import OAuth2PasswordRequestForm #*
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authertication']) #

@router.post('/login', response_model=schemas.Token) #*
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), #* with the password request form you need to use Body/form-data of postman
            db: Session=Depends(database.get_db)
): #* by using this you have to use form-data in postman
# def login(user_credentials: schemas.UserLogin, db: Session=Depends(database.get_db)):

    # the format the passwordrequestform has: #*
    # {
    #     username = 'adfas',
    #     password = 'dfsfgsg'
    # }
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #*

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password): # user.password here is the hashed stored password returned back from database
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #create a token
    access_token = oauth2.create_access_token(data={"user_id":user.id}) #* you can add more things like role, etc.

    # return token
    return {"access_token": access_token, "token_type":"bearer"}


