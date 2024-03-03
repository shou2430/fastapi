from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, utils
from ..database import get_db
from ..schemas import UserCreate, UserOut

router = APIRouter(
    prefix="/user"
)


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.get_hashed_password(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# 不確定為啥要設置這個 route
@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user
