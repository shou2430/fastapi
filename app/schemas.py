from pydantic import BaseModel


# use a class to define a post should look like
class PostBase(BaseModel):
    title:str
    content: str
    published: bool = True


# use a class to define a post should look like when it's being created
class PostCreate(PostBase):
    pass


# use a class to define a post should look like when it's being updated
class PostUpdate(PostBase):
    published: bool


# define a class for post when it's being requested
class PostReponse(PostBase):

    class Config:
        orm_mode = True