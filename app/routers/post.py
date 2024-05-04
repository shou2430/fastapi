from typing import Optional
from ..schemas import PostCreate, PostUpdate, PostReponse, PostOut
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, oauth2


router = APIRouter(
    prefix="/posts"
)

@router.get("/", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(limit, search)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).outerjoin(
        models.Votes, models.Post.id == models.Votes.post_id).group_by(models.Post.id)
    print(result)
    result.all()
    return result


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).\
        outerjoin(models.Votes, models.Post.id == models.Votes.post_id).\
        filter(models.Post.id == id).\
        group_by(models.Post.id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=PostReponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)  # add the new post to the database
    db.commit()  # commit the changes to the database
    db.refresh(new_post)  # refresh the new_post to get the id

    return new_post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    result = db.query(models.Post).filter(models.Post.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesn't exist")

    if result.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you are not authorized to delete this post")

    db.query(models.Post).filter(models.Post.id == id).delete(
        synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostReponse)
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print('current user: ', type(current_user))
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesn't exist")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you are not authorized to update this post")
    
    print('legal')
    db.query(models.Post).filter(models.Post.id == id).update(
        post.model_dump())
    db.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    print('updated_post', updated_post)
    return updated_post
