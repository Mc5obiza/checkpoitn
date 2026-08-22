import asyncio
import functools

def timeout(time=10):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=time)
            except asyncio.TimeoutError:
                return {
                    "answer": "The AI service is taking too long. Please try again.",
                    "model": "timeout",
                    "tokens_used": 0
                }
        return wrapper
    return decorator

# Model values that indicate a transient failure worth retrying.
RETRYABLE_MODELS = {"timeout", "rate limited"}

def retry(max_retries=2):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = None
            for attempt in range(max_retries + 1):
                result = await func(*args, **kwargs)
                if result.get("model") not in RETRYABLE_MODELS:
                    return result
                if attempt < max_retries:
                    await asyncio.sleep(1)
            return result
        return wrapper
    return decorator