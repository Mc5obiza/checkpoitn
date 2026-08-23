from langgraph.graph import StateGraph, START, END,MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage,SystemMessage
from typing import TypedDict    
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from utility.tool import google_search, calculator

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key is None:
    raise ValueError("Key is not Available ")
client = ChatOpenAI(api_key=key,base_url="https://openrouter.ai/api/v1",model="openrouter/free",temperature=0.3)#type: ignore
tools = [google_search,calculator]
model_with_tools = client.bind_tools(tools) 
SYSTEM_PROMPT = """
You are a helpful AI assistant.

You have access to tools for:
- performing mathematical calculations
- searching the web for current or unknown information

Use the calculator whenever the user asks for a mathematical calculation.
Do not calculate arithmetic yourself when the calculator can be used.

Use google_search when the user asks for current information or
information that may require web research.

After receiving a tool result, analyze it and decide whether another
tool call is necessary before giving the final answer.
"""
tools_used = []
class State(MessagesState):
    pass 
def call_model(state):
    response = model_with_tools.invoke([SystemMessage(SYSTEM_PROMPT),*state["messages"]])
    return {
        "messages":[response]
    }
tool_node = ToolNode(tools,handle_tool_errors=True)
graph = StateGraph(State)

graph.add_node("llm",call_model)
graph.add_node("tools",tool_node)
graph.add_edge(START,"llm")
def should_continue(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        tools_used.append(last_message.tool_calls)
        print("It s tool call")
        return "tools"
    else:
        print("There is no tool call")
    return END
def fall_back(state):
    last_message = state["messages"][-1]
    if not last_message.content:
        return "retry"
    return "end"

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools":"tools",
        END:END
    }
)    
graph.add_conditional_edges(
    "llm",
    fall_back,
    {
        "retry":"llm",
        "end":END
    }
)
graph.add_edge("tools","llm")
agent = graph.compile()
messages = ["What is sqrt(144) + 5?","what is 5/0","How can I learn Agentic AI "]
for q in messages:
    print("Human:",q,end="\n\n")
    result = agent.invoke({
        "messages":[HumanMessage(content=q)]
    })
    for message in result["messages"]:
        print("\nTYPE:", type(message).__name__)
        print("CONTENT:", message.content)

        if hasattr(message, "tool_calls"):
            print("TOOL CALLS:", message.tool_calls)
print(tools_used)