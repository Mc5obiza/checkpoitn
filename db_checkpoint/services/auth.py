from jose import jwt,JWTError
from datetime import datetime, timezone, timedelta 
import bcrypt
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("There is No secret key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30

def hash_password(pwd:str)->str:
    return bcrypt.hashpw(
        pwd.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(pwd:str,pwd_hash:str)->bool:
    return bcrypt.checkpw(
        pwd.encode("utf-8"),
        pwd_hash.encode("utf-8")
    )

def create_access_token(user_id):
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MIN)
    paylaod = {
        "sub" : str(user_id),
        "exp" : expire
    }
    return jwt.encode(paylaod,SECRET_KEY,algorithm=ALGORITHM)
def decode_access_token(token):
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload["sub"]

        if user_id is None:
            return None
        return int(user_id)
    except JWTError as je:
        return None
def get_current_user(token: str=Depends(oauth2_schema),db : Session=Depends(get_db)):
    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(status_code=401,detail="Invalid or expired token")

    user = db.get(User,user_id)

    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user