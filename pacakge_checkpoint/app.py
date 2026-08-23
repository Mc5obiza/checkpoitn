import os

import gradio as gr
import requests


API_URL = os.getenv("API_URL", "http://localhost:8000/invoke")


def chat_with_agent(user_input: str) -> str:
    payload = {"input": {"input": user_input}}
    response = requests.post(API_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json().get("output", "Error: no output returned")


demo = gr.Interface(
    fn=chat_with_agent,
    inputs=gr.Textbox(lines=2, placeholder="Ask me anything..."),
    outputs=gr.Textbox(),
    title="LangChain Agent with Gradio",
)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("GRADIO_PORT", "7860")),
    )