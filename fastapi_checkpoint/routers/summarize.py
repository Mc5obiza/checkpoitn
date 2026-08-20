from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from services.summarize import summarize

class SummaryRequest(BaseModel):
    text : str = Field(...,min_length=10,max_length=1500)
    max_bullets : int = Field(gt=1)
class ResponseModel(BaseModel):
    answer : str
    model : str
    tokens_used : int

router = APIRouter(prefix="/summarize",tags=["summarize"])
@router.post("",response_model=ResponseModel)
def get_summary(request:SummaryRequest):
    clean_text = request.text.strip()
    if not clean_text:
        raise HTTPException(status_code=400,detail="Can not pass empty text to summarize")
    response = summarize(clean_text,request.max_bullets)
    return ResponseModel(**response)