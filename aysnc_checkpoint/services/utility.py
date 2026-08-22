import asyncio
import functools

def timeout(time=10):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args,**kargs):
            try:
                result = await asyncio.wait_for(
                    func(*args,**kargs),
                    timeout=time
                )
                return result
            except asyncio.TimeoutError as te:
                return {
                    "answer" : "The AI service is taking too long. Please try again.",
                    "model" : "timeout",
                    "tokens_used" : 0
                }
        return wrapper
    return decorator

def retry(max_retries=2):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                result = await func(*args, **kwargs)
                if result["model"] not in ("rate limited", "timeout"):
                    return result
                if attempt < max_retries:
                    await asyncio.sleep(1)
            return result
        return wrapper
    return decorator
