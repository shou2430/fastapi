from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2


router = APIRouter(tags=["authentications"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    OAuth2PasswordRequestForm 在收到請求時會自動解析，提取出 username 和 password、scope、grant_type 等信息。
    user_credentials: OAuth2PasswordRequestForm = Depends() 這行代碼的意思是，當這個 login 函數被調用時，
    FastAPI 會自動解析請求，提取出 username 和 password，並將其傳遞給 user_credentials 這個參數。
    """
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create a token 
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}