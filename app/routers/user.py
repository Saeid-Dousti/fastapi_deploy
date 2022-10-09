# 7:28 shortenning the path

from fastapi import (  # to get status code
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,
    APIRouter, #* to access FASTAPI from the main_26.py
)
from sqlalchemy.orm import Session
from .. import models, schemas, utils #*
from ..database import get_db #*

router = APIRouter(
    prefix="/users", #*
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  # *
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password -  user.password
    # hashed_password = pwd_context.hash(user.password) #
    # user.password = hashed_password #

    user.password = utils.hash(user.password) #

    new_user = models.User(**user.dict())  
    db.add(new_user)  # add my_post to database
    db.commit()  # save it
    db.refresh(
        new_user
    )  # finally get what is saved in the table back which basically does the RETURNING thing in SQL

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)  #*
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" User with id: {id} not found")

    return user
