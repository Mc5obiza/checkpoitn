import os
from dotenv import load_dotenv
from mistralai.client import Mistral
import subprocess
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("There is no such API KEY in the .env Check your file")
client = Mistral(api_key=API_KEY)
SYSTEM_PROMPT = """
You are a friendly and supportive study tutor.

Your role is to help the student learn, understand, and improve—not just give answers.

* Explain concepts simply and clearly, using easy language and examples.
* Break difficult topics into small, manageable steps.
* Encourage the student and maintain a positive, patient tone.
* When the student makes a mistake, correct it gently and explain why.
* Ask guiding questions when they can help the student discover the answer themselves.
* Adapt explanations to the student's apparent level of knowledge.
* Prefer understanding and reasoning over memorization.
* When useful, give short exercises, examples, or practice questions.
* Do not overwhelm the student with unnecessary information.
* If the student asks for a direct answer, provide it clearly, then briefly explain the reasoning.
* Act like a study partner who helps the student become more independent and confident.

"""
def call_ai():
    try:
        client = Mistral(api_key=API_KEY)
    except Exception as e:
        print(f"Error occurred while initializing Mistral client: {e}")
        return

    message_history=[{"role":"system","content":SYSTEM_PROMPT}]
    token_spent = {"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}
    print("Hi!! How can i help you?")
    while True:
        print("\n")
        user_input = input(">> ")
        if user_input.split(" ")[0].startswith("\\"):
            if user_input.startswith("\\exit") :
                break
            if user_input.startswith("\\clear"):
                message_history = [message_history[0]]
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
                stream = client.chat.stream(
                    model = "mistral-small-latest",
                    messages = message_history,
                    temperature=0.3,
                    max_tokens=2000,
                    stream=True
                )
                response = ""
                for chunk in stream:
                    content = chunk.data.choices[0].delta.content
                    if content:
                        print(content,end="",flush=True)
                        response+=content
                    if chunk.data.usage:
                        token_spent["completion_tokens"]+=chunk.data.usage.completion_tokens
                        token_spent["prompt_tokens"]+=chunk.data.usage.prompt_tokens
            except Exception as e:
                print(f"Unable to get an AI response. Check your internet connection or API key: {e}")
                return

            message_history.append({"role":"assistant","content":response})
call_ai()
