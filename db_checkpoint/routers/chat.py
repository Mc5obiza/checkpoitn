from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from services.ai import call_llm
from services.auth import get_current_user
from models import User
from database import get_db
from services.curd import create_conversation,create_session
router = APIRouter(prefix="/chat",tags=["chat"])
class ChatRequest(BaseModel):
    message :str = Field(...,min_length=1,max_length=200)
class ChatResponse(BaseModel):
    answer:str
    model:str
    tokens_used:int
@router.post("",response_model=ChatResponse)
def chat(request:ChatRequest,user : User = Depends(get_current_user),session_id = None,db : Session = Depends(get_db)):
    clean_msg = request.message.strip()
    if not clean_msg:
        raise HTTPException(status_code=400,detail="Message cannot be empty")
    result = call_llm(clean_msg)
    if session_id is None:
        session_id = create_session(db,user.id)
    create_conversation(db,session_id,request.message,result["answer"])
    return ChatResponse(**result)


