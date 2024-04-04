from jose import JWTError, jwt
from datetime import datetime, timedelta

# sercret key to encode and decode the token
SECRET_KEY = "d3f9b3d7c0d0b6e7e8d9f6e9d5b2e4d5"

# algorithm to encode and decode the token
ALGORITHM = "HS256"

# define the token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
