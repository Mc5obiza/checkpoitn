from dotenv import load_dotenv
import os
from openai import AsyncOpenAI,AuthenticationError,RateLimitError
import asyncio
from .utility import retry , timeout
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("There is no such OPENAI_API_KEY")
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)
SYSTEM_PROMPT = """

You are a helpful learning assistant.

Explain concepts clearly and use examples when useful.

If the question is unclear, ask for clarification.

"""
@retry(2)
@timeout(10)
async def call_llm(message:str)->dict:
    try:
        response = await client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role":"system","content":SYSTEM_PROMPT},{"role": "user", "content": message}],
        temperature=0.3,
        max_tokens=700  
        )
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else 0
        return {
            "answer":answer,
            "model":response.model,
            "tokens_used":tokens_used
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
    