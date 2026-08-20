from dotenv import load_dotenv
from openai import OpenAI
import os
import subprocess
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A777AAA")
def call_ai():
    try:
        client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    except Exception as e:
        print(f"Error occurred while initializing OpenAI client: {e}")
        return

    message_history=[]
    token_spent = {"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}
    print("Hi!! How can i help you?")
    while True:
        print("\n")
        user_input = input(">> ")
        if user_input.split(" ")[0].startswith("\\"):
            if user_input.startswith("\\exit") :
                break
            if user_input.startswith("\\clear"):
                message_history = []
                subprocess.run(["cls"],shell=True)
                print("Hello there again")
            elif user_input.startswith("\\help"):
                print("\\exit : quit the conversation\n\\clear : Delete the whole conversation\n\\check_usage : How much tokens spent")
            elif user_input.startswith("\\check_usage"):
                print("SPENNT",token_spent)
            else:
                print("Unrecognized Command")
        else:
            message_history.append({"role":"user","content":user_input})
            try:
                stream = client.chat.completions.create(
                    model = "openrouter/free",
                    messages = message_history,
                    stream=True
                )
            except Exception as e:
                print(f"Error occurred while fetching AI response: {e}")
                return

            response = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    print(content,end="",flush=True)
                    response+=content
                if chunk.usage:
                    token_spent["completion_tokens"]+=chunk.usage.completion_tokens
                    token_spent["prompt_tokens"]+=chunk.usage.prompt_tokens
                    token_spent["total_tokens"]+=chunk.usage.total_tokens

            message_history.append({"role":"assistant","content":response})
call_ai()
            

