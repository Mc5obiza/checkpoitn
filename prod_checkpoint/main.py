from fastapi import FastAPI
from datetime import datetime ,timezone
from routers import chat, quizz, summarize
app = FastAPI(
    title="FASTAPI CHECKPOINT",
    description="Checkpoint GoMyCode FastAPI",
    version="1.0.0"
)
app.include_router(chat.router)
app.include_router(quizz.router)
app.include_router(summarize.router)

@app.get("/health")
def health():
    return {
        "status":"ok",
        "message":"API is running",
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "version" : "1.0.0"
    }