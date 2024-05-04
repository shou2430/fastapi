from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# use a class to define a user should look like when it's being created
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# filter the sent back info after the user is created
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# use a class to define a user should look like when it's being logged in
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# use a class to define a post should look like
class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    owner_id: int


# use a class to define a post should look like when it's being created
class PostCreate(PostBase):
    pass


# use a class to define a post should look like when it's being updated
class PostUpdate(PostBase):
    published: bool


# define a class for post when it's being requested
class PostReponse(PostBase):
    owner: UserOut
    
    class Config:
        orm_mode = True


# define a class for post when it's being requested
class PostOut(BaseModel):
    Post: PostReponse
    votes: int

    class Config:
        orm_mode = True

# define a class for vote when it's being created
class VoteInfo(BaseModel):
    post_id: int
    switch: int
