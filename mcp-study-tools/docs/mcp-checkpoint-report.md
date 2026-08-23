# MCP Checkpoint Report

## Architecture

This project uses the Model Context Protocol with the Python `FastMCP` server implementation.

- `server.py` creates a `FastMCP` instance named `project-tools`.
- The client in `client-test.py` starts the server through an MCP stdio transport.
- `ClientSession` initializes the connection and discovers the available tools with `list_tools()`.
- The client asks an OpenRouter model to select a tool, validates the returned tool name and arguments locally, and calls the selected tool with `call_tool()`.
- Tool results are returned to the client as MCP content.
- The server source currently defines the MCP handlers but does not call `mcp.run()` when executed as a script. As a result, the current client test exits during initialization with `McpError: Connection closed`.

## Tools

| Tool | Purpose | Inputs |
| --- | --- | --- |
| `explain_topic` | Return a structured explanation outline for a topic. | `topic: str`, optional `level: str` |
| `create_study_plan` | Create a study plan constrained to 1-14 days. | `topic: str`, optional `days: int` |
| `generate_revision_checklist` | Return five revision prompts for a topic. | `topic: str` |

The server also exposes the `quiz_prompt` prompt, which generates instructions for multiple-choice questions. It is not included in the tool list because prompts are a separate MCP capability.

## Resource URI

- `project://course-outline`

The resource returns:

> Core modules: AI foundations, APIs, backend, database, RAG, agents, MCP, deployment.

## Tool Failure And Server Response

A deliberate invalid call was made to `explain_topic` with an empty topic:

```python
server.explain_topic("")
```

The server responds with a structured failure rather than raising an exception:

```python
{
    "status": False,
    "error": "topic cannot be empyt"
}
```

The spelling of `empyt` reflects the current server implementation.

## Client Test Output

The command was run in the `agents_env` conda environment:

```text
conda activate agents_env
python client-test.py
```

Observed result:

```text
ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
...
mcp.shared.exceptions.McpError: Connection closed

Command exited with code 1
```

The failure occurs at `session.initialize()`, before the client can list tools or call the model-selected tool. Both Python files import and compile successfully; the connection closes because the executed server process terminates without entering the MCP server run loop.

## Security Notes

- Keep `OPENAI_API_KEY` in `.env` or another secret manager; do not commit it to source control.
- The client uses `load_dotenv()` and sends user-request routing requests to OpenRouter. Treat user requests and model responses as data shared with that provider.
- Tool names are checked against the server-discovered allowlist before invocation.
- Tool arguments are checked for object shape and required fields, and `create_study_plan.days` must be an integer.
- The server bounds study plans to 1-14 days, which limits resource use from an oversized request.
- Empty topics are rejected by the tools instead of being processed.
- Stdio is local process communication; if the server is later exposed over a network transport, add authentication, authorization, input limits, and encrypted transport.
- The current client prints tool results and exceptions. Avoid logging secrets or sensitive user content in production.
