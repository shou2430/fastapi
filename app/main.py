import psycopg2
import time

from psycopg2.extras import RealDictCursor
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .schemas import PostCreate, PostUpdate, PostReponse
from .database import get_db, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostReponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post) # add the new post to the database
    db.commit() # commit the changes to the database
    db.refresh(new_post) # refresh the new_post to get the id

    return new_post

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesn't exist")
    
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit() 

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):

    updated_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesn't exist")   
    
    db.query(models.Post).filter(models.Post.id == id).update(post.model_dump())
    db.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()

    return {"data": updated_post}     
