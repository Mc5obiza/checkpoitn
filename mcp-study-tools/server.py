from mcp.server.fastmcp import FastMCP
mcp = FastMCP("project-tools")
def clamp_days(days: int) -> tuple[int, str | None]:
    if days < 1:
        return 1, "Days was too low, so it was changed to 1."
    if days > 14:
        return 14, "Days was too high, so it was changed to 14."
    return days, None
@mcp.tool()
def explain_topic(topic : str, level : str = "beginner")->dict:
    if not topic.strip():
        return {
            "status":False,
            "error":"topic cannot be empyt"
        }
    allowed_levels = {"beginner","intermediate","advanced"}
    if level not in allowed_levels:
        level = "beginner"
    return {
        "status":True,
        "topic":topic,
        "level":level,
        "format":[
            "Definition",
            "Simple explanation",
            "Practical example",
            "Common mistakes",
            "Short summary"
        ]
    }
@mcp.tool()
def create_study_plan(topic: str, days: int = 3) -> dict:
    """Create a safe study plan between 1 and 14 days."""
    if not topic.strip():
        return {"ok": False, "error": "Topic cannot be empty."}

    safe_days, warning = clamp_days(days)
    plan = []

    for day in range(1, safe_days + 1):
        plan.append({
            "day": day,
            "focus": f"Study part {day} of {topic}",
            "task": f"Review {topic} for 45 minutes.",
            "practice": "Write 5 key points and answer 3 questions."
        })

    return {
        "ok": True,
        "topic": topic,
        "days": safe_days,
        "warning": warning,
        "plan": plan
    }


@mcp.tool()
def generate_revision_checklist(topic: str) -> dict:
    """Generate a short checklist for reviewing a topic."""
    if not topic.strip():
        return {"ok": False, "error": "Topic cannot be empty."}

    return {
        "ok": True,
        "topic": topic,
        "checklist": [
            f"Define {topic} in your own words.",
            f"List the main components of {topic}.",
            f"Explain one practical use case for {topic}.",
            f"Identify two common mistakes related to {topic}.",
            f"Create one mini example using {topic}."
        ]
    }
@mcp.resource("project://course-outline")
def course_outline() -> str:
    return "Core modules: AI foundations, APIs, backend, database, RAG, agents, MCP, deployment."


@mcp.prompt()
def quiz_prompt(topic: str, num_questions: int = 5) -> str:
    return f"Create {num_questions} multiple-choice questions about {topic}. Include answers and explanations."
if __name__ == "__main__":
    mcp.run(transport="stdio")