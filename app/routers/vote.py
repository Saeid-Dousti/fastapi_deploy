# 9:35

from fastapi import (  # to get status code
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,
    APIRouter, 
)
from sqlalchemy.orm import Session

from app import database #
from .. import models, schemas, oauth2 #
from ..database import get_db #


router = APIRouter(
    prefix='/vote', 
    tags=['Vote']
) #

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post found")

    elif vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}", )
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()  # save it
        return {"message": "successfully added a vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {current_user.id} has not voted on post {vote.post_id}", )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted a vote"}

    

