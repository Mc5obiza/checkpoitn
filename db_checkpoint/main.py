from fastapi import FastAPI, Depends,HTTPException
from datetime import datetime ,timezone
from routers import chat
from database import get_db,engine,Base
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from services.curd import UserCreate,create_user,authenticate_user
from services.auth import create_access_token

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="FASTAPI CHECKPOINT",
    description="Checkpoint GoMyCode FastAPI",
    version="1.0.0"
)
app.include_router(chat.router)

@app.get("/health")
def health():
    return {
        "status":"ok",
        "message":"API is running",
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "version" : "1.0.0"
    }

@app.get("/test-db")
def db_test(db : Session = Depends(get_db)):
    return {"database":"connected"}
@app.post("/signup")
def signup(user : UserCreate,db : Session = Depends(get_db)):
    response = create_user(db,user)
    if "status" in response.keys():
        raise HTTPException(status_code=409,detail="User already exists")
    return response
@app.post("/login")
def login(user : UserCreate, db : Session = Depends(get_db)):
    response = authenticate_user(db,user)
    if response["user"] is None:
        raise HTTPException(status_code=404,detail=response["message"])   
    token = create_access_token(response["user"].id)
    return {
        "access_token":token,
        "token_type":"bearer"
    }
    