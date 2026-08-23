from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field
from llm.llm import chose_llm
import json
llm = chose_llm()
router = APIRouter(prefix="/chat",tags=["chat"])
async def event_generator(request):
    async for event in llm(request.message):
        yield json.dumps(event) + "\n"

class ChatRequest(BaseModel):
    message :str = Field(...,min_length=1,max_length=200)
class ChatResponse(BaseModel):
    type : str
    model:str
    tokens_used:int
@router.post("")
def chat(request:ChatRequest):
    clean_msg = request.message.strip()
    if not clean_msg:
        raise HTTPException(status_code=400,detail="Message cannot be empty")
    return StreamingResponse(
        event_generator(request.message),
        media_type="application/x-ndjson"
    )


