from fastapi import APIRouter,HTTPException 
from pydantic import BaseModel,Field
from services.ai import call_llm

router = APIRouter(prefix="/chat",tags=["chat"])
class ChatRequest(BaseModel):
    message :str = Field(...,min_length=1,max_length=200)
class ChatResponse(BaseModel):
    answer:str
    model:str
    tokens_used:int
@router.post("",response_model=ChatResponse)
async def chat(request:ChatRequest):
    clean_msg = request.message.strip()
    if not clean_msg:
        raise HTTPException(status_code=400,detail="Message cannot be empty")
    result = await call_llm(clean_msg)
    return ChatResponse(**result)


