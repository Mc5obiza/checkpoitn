from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User, Message, Conversation
from .auth import verify_password,hash_password,create_access_token,decode_access_token
from fastapi import HTTPException
class UserCreate(BaseModel):
    email :str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    pwd : str = Field(...,min_length=8)

def create_user(db : Session, user : UserCreate):
    db_user =  User(
        email = user.email,
        password_hash = hash_password(user.pwd)
    )
    query = select(User).where(User.email == db_user.email)
    selected_user = db.scalar(query)
    if selected_user is not None:
        return {
            "status" : "failed",
            "message" : "user Exists"
        }
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token(db_user.id)
    return {
        "access_token":token,
        "token_type":"bearer"
    }
def authenticate_user(db:Session, user :UserCreate):
    query = select(User).where(User.email == user.email)
    selected_user = db.scalar(query)
    if selected_user is None:
        return {
            "status":"didn t exist",
            "message":"Incorrect password or email",
            "user":None
        }
    if verify_password(user.pwd,selected_user.password_hash):
        return  {
            "status":"Yes",
            "message":"found user",
            "user":selected_user
        }
    else:
        return {
            "status":"error",
            "message":"Incorrect password or email",
            "user":None
        }
def create_session(db:Session, user_id:str ):
    query = select(User).where(User.id == user_id)
    selected_user = db.scalar(query)
    if selected_user is None:
        raise HTTPException(status_code=404,detail="User doesn t exist")
    db_session = Conversation(
        user_id = user_id,
        title = "placeholder we will add AI Title one day"
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session.id
def create_conversation(db:Session,conversation_id:str,request:str,response:str):
    query = select(Conversation).where(Conversation.id == conversation_id)
    selected_conversation = db.scalar(query)
    if selected_conversation is None:
        raise HTTPException(status_code=404,detail="Conversation doesn t exist")
    def add_message(role,messgae):
        db_messgae = Message(
            conversation_id = conversation_id,
            role = role,
            content = messgae
        )
        db.add(db_messgae)
        db.commit()
        db.refresh(db_messgae)
    add_message("user",request)
    add_message("assistant",response)
   