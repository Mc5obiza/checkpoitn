from dotenv import load_dotenv
from openai import OpenAI,AuthenticationError,RateLimitError
from pydantic import BaseModel,Field
class Question(BaseModel):
    question :str=Field(...)
    options:list[str]
    correct_answer:str
class Quizz(BaseModel):
    quizz:list[Question]
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Couldn t find the API key")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)
SYSTEM_PROMPT = """You are a quiz generator.
Generate multiple-choice quiz questions.
Each question must have exactly 4 options and exactly one correct answer.
Make the questions relevant to the requested topic and factually accurate."""
def generate_quiz(number:int,topic:str):
    try:
        user_message = f"Generate {number} questions about {topic}."
        response = client.beta.chat.completions.parse(
            model="openrouter/free",
            messages=[{"role":"system","content":SYSTEM_PROMPT},{"role": "user", "content": user_message}],
            temperature=0.3,
            max_tokens=700,
            response_format=Quizz
            )
        event = response.choices[0].message.parsed
        return {
            "answer":event,
            "model":response.model,
            "tokens_used":response.usage.total_tokens if response.usage else 0
        }
    except AuthenticationError as ae:
        return {
            "answer":"a77aa",
            "model":"error",
            "tokens_used":0
        }
    except RateLimitError as rle:
        return {
            "asnwer" : "abay",
            "model":"mach8ol",
            "tokens_used":0
        }
    except Exception as e:
        return {
            "answer":"allaho a3lem",
            "model":"maan3rifchi",
            "tokens_used":0
        }
    

    
    
    