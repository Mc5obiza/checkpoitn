from openai import OpenAI,RateLimitError,AuthenticationError
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("There is no OPENAI API KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)
SYSTEM_PROMPT = """You are a text summarization assistant.

Your task is to summarize the user's provided text into a short, clear list of key points.

Rules:

* Return only the most important information.
* Use concise bullet points.
* Do not add information that is not present in the input text.
* The number of bullet points must not exceed the maximum specified by the user.
* Prefer fewer bullets when the text does not contain enough distinct key points.
* Keep each bullet short and easy to understand.
* Preserve important names, facts, numbers, and conclusions.
* Do not include an introduction, conclusion, or unnecessary commentary.
"""
def summarize(text:str,max_bullets:int)->dict:
    try:
        user_prompt = f"""Summarize the following text into a maximum of {max_bullets} concise bullet points.

                        Text:
                        {text}  

                        Return the summary as a list of bullet points."""
        response = client.chat.completions.create(
                model="openrouter/free",
                messages=[{"role":"system","content":SYSTEM_PROMPT},{"role": "user", "content": user_prompt}],
                temperature=0.3,
                max_tokens=2000
                )
        answer = response.choices[0].message.content
        return {
            "answer":answer,
            "model":response.model,
            "tokens_used" : response.usage.total_tokens if response.usage else 0
        }
    except AuthenticationError as ae:
            return {
                "answer":"Authentification Error check the API Key",
                "model":"error",
                "tokens_used":0
            }
    except RateLimitError as rle:
            return{
                "answer":"Too much requests the model is right now busy",
                "model":"rate limited",
                "tokens_used":0
            }
    except Exception as e:
            return {
                "answer":"Unexpected Error",
                "model":"error",
                "tokens_used":0
            }