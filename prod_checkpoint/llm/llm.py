from mistralai.client import Mistral
from dotenv import cli, load_dotenv
import os
from openai import AsyncOpenAI,AuthenticationError,RateLimitError
from sympy import re
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER")
async def call_llm_openai(message:str,**kwargs):
    try:
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
        stream = await client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role":"system","content":SYSTEM_PROMPT},{"role": "user", "content": message}],
        stream=True,
        stream_options={"include_usage": True},
        **kwargs
        )
        usage = None
        model = None
        async for event in stream:
            model = event.model
            if event.choices:
                content = event.choices[0].delta.content
                
                if content:
                    yield {"type":"content","content":content}
                if event.usage:
                    usage = event.usage
        yield {
            "type":"done",
            "model":model,
            "token_used":usage.total_tokens
        }   

            
            
    except AuthenticationError as ae:
        yield {
            "type":"Authentication error",
            "model":"Not authenticated",
            "tokens_used":0
        }
        
    except RateLimitError as rle:
        yield {
                    "type":"The model is not availabe",
                    "model":"Rate hit",
                    "tokens_used":0
                }
        
    except Exception as e:
        yield {
                    "type":"Internal error",
                    "model":"maha3ah",
                    "tokens_used":0
                }
async def call_llm_mistral(message: list,**kwargs):
    try:
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError("There is no such MISTRAL_API_KEY")

        client = Mistral(api_key=api_key)

        SYSTEM_PROMPT = """
        You are a helpful learning assistant.

        Explain concepts clearly and use examples when useful.

        If the question is unclear, ask for clarification.
        """

        stream = await client.chat.stream_async(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            **kwargs
        )

        model = None
        usage = None

        async for event in stream:
            data = event.data

            model = data.model or model

            if data.choices:
                content = data.choices[0].delta.content

                if content:
                    yield {
                        "type": "content",
                        "content": content
                    }

            if data.usage:
                usage = data.usage

        yield {
            "type": "done",
            "model": model,
            "tokens_used": usage.total_tokens if usage else 0
        }

    except Exception as e:
        yield {
            "type": "error",
            "error": "internal_error",
            "message": str(e),
            "model": None,
            "tokens_used": 0
        }
def chose_llm():
    if LLM_PROVIDER == "mistralai":
        return call_llm_mistral
    if LLM_PROVIDER == "openai":
        return call_llm_openai
    raise ValueError("The provider is not availabe yet")