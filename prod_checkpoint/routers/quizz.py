from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from services.quizz import Quizz, generate_quiz
class RequestQUizz(BaseModel):
    subject : str = Field(...,min_length=1,max_length=500)
    number : int = Field(...,gt=1,lt=10)
class ResponseModel(BaseModel):
    answer : Quizz
    model : str
    tokens_used : int
router = APIRouter(prefix="/quizz",tags=["quizz"])
@router.post("",response_model=ResponseModel)
def get_quizz(request:RequestQUizz):
    clean_subject = request.subject.strip()
    if not clean_subject:
        raise HTTPException(status_code=400,detail="Subject must not be an empty string")
    response = generate_quiz(request.number,clean_subject)
    return ResponseModel(**response)
