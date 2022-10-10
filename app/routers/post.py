# 10:15, Join queries, get the votes of the posts

from optparse import Option
from typing import List, Optional #
from fastapi import (  # to get status code
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,
    APIRouter, 
)
from sqlalchemy.orm import Session #
from sqlalchemy import func #10:15
from .. import models, schemas, oauth2 #
from ..database import get_db #

router = APIRouter(
    prefix='/posts', 
    tags=['Posts']
) #

@app.get("/")
def root():
    return {"message": "Hello World"}

# @router.get(
#     "/", response_model=List[schemas.Post]
# )  #* 10:16 modified the response model
@router.get(
    "/", response_model=List[schemas.PostOut]
)  #* 10:16 modified the response model
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""): #* 8:41, query parameter
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id group by posts.id
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #* 8:43
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #* 10:15
    
    # print(results)

    return posts  # this will convert the list to JSON


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  #
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user = Depends(oauth2.get_current_user) ):  #

    # print('\n\n\n', current_user.email) 
    # print('\n\n\n', post) 
    # my_post = models.Post(**post.dict())  #
    my_post = models.Post(owner_id=current_user.id, **post.dict())  # 8:19 no need to get owner_id from postman
    db.add(my_post)  # add my_post to database
    db.commit()  # save it
    db.refresh(
        my_post
    )  # finally get what is saved in the table back which basically does the RETURNING thing in SQL

    return my_post


# getting path parameter from a get request
# @router.get("/{id}", response_model=schemas.Post)  #
@router.get("/{id}", response_model=schemas.PostOut)  #* 10:28
def get_post(id: int, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):  #

    # cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id),) ) # we convert the int id back to a string after making sure it is a valid path parameter, the comma fixes the problem of ids >9
    # post = cursor.fetchone()
    # # print(post)

    # post = (
    #     db.query(models.Post).filter(models.Post.id == id).first()
    # )  # filter is equivalent of a WHERE,
    # .all() will cause postgres to keep looking while we just know that just one is post with id is gonna exist so we use .first()
    # print(post)

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first() #* 10:28

    if not post:
        # response.status_code = 404 # this is not a proper way
        # response.status_code = status.HTTP_404_NOT_FOUND # this is not a proper way
        # return {'message': f'post with id: {id} was not found'} #
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    # if post.owner_id != current_user.id:  # 8:32
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"not authorized to perform requested action",
    #     )

    return post


# delete one post
@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT
)  # 8:23
def delete_post(id: int, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):  #

    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),) ) # we convert the int id back to a string after making sure it is a valid path parameter, the comma fixes the problem of ids >9
    # post = cursor.fetchone()#
    # # print(post)
    # conn.commit()

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )  # we just get the query and not the post itself

    if post_query.first() == None:  #
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )
    
    if post_query.first().owner_id != current_user.id:  # 8:22
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform requested action",
        )

    post_query.delete(
        synchronize_session=False
    )  # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#selecting-a-synchronization-strategy
    db.commit()  # save it

    # return {'message': f'the post with id {id} was successfullt deleted '} # no message should be returned back
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )  # basically this says that there should not be anything to return


# update one post
@router.put("/{id}", response_model=schemas.Post)  # 8:23
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):  #

    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #         (post.title, post.content, post.published, str(id), ) ) # we convert the int id back to a string after making sure it is a valid path parameter, the comma fixes the problem of ids >9
    # post = cursor.fetchone()#
    # conn.commit()

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )  # we just get the query and not the post itself

    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )

    if post_query.first().owner_id != current_user.id:  # 8:22
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform requested action",
        )

    post_query.update(post.dict(), synchronize_session=False)  #
    db.commit()  # save it

    return post_query.first()