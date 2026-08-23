import os

import uvicorn
from fastapi import FastAPI
from langserve import add_routes

from agent import agent


app = FastAPI(title="LangChain Agent API")
add_routes(app, agent, path="/")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )