import asyncio
import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

client = OpenAI(api_key=api_key,base_url="https://openrouter.ai/api/v1")


def choose_tool(user_request: str, tool_names: list[str]) -> dict[str, Any]:
    prompt = f"""
You are choosing one MCP tool for a user request.

Available tools:
{tool_names}

User request:
{user_request}

Return JSON only in this format:
{{
  "tool_name": "name_here",
  "arguments": {{}}
}}

Rules:
- Use create_study_plan when the user asks for a plan.
- Use explain_topic when the user asks for an explanation.
- Use generate_revision_checklist when the user asks for a checklist.
- Do not invent tool names.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    return json.loads(content)


def validate_tool_decision(
    decision: dict[str, Any],
    allowed_tools: list[str]
) -> tuple[str, dict[str, Any]]:
    tool_name = decision.get("tool_name")
    arguments = decision.get("arguments", {})

    if not tool_name:
        raise ValueError("The model did not return a tool_name.")

    if tool_name not in allowed_tools:
        raise ValueError(f"Tool not allowed: {tool_name}")

    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a JSON object.")

    if tool_name == "create_study_plan":
        if "topic" not in arguments:
            raise ValueError("create_study_plan requires a topic.")
        if "days" in arguments and not isinstance(arguments["days"], int):
            raise ValueError("create_study_plan days must be an integer.")

    if tool_name == "explain_topic" and "topic" not in arguments:
        raise ValueError("explain_topic requires a topic.")

    if tool_name == "generate_revision_checklist" and "topic" not in arguments:
        raise ValueError("generate_revision_checklist requires a topic.")

    return tool_name, arguments


async def main():
    user_request = "Create a 3-day plan to learn MCP."

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            allowed_tools = [tool.name for tool in tools_response.tools]

            print("Available tools:", allowed_tools)

            try:
                decision = choose_tool(user_request, allowed_tools)
                print("arguments:", decision["arguments"])
                tool_name, arguments = validate_tool_decision(decision, allowed_tools)
                
                result = await session.call_tool(tool_name, arguments)

                print("\nUser request:", user_request)
                print("Tool chosen:", tool_name)
                print("Arguments:", arguments)
                print("Tool result:", result.content)

            except json.JSONDecodeError:
                print("The model did not return valid JSON.")
            except Exception as error:
                print("Agent workflow failed:", str(error))


if __name__ == "__main__":
    asyncio.run(main())