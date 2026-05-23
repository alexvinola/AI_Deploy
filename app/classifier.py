"""
Clasificador de tickets de soporte técnico.
Versión limpia de L3 (tool use) de AI Workflows, lista para producción.
"""

import json
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-5"

# ─────────────────────────────────────────────
# Tools (mocks — en producción conectarías Jira, PagerDuty, etc.)
# ─────────────────────────────────────────────

TOOLS = [
    {
        "name": "search_similar_tickets",
        "description": (
            "Search for similar support tickets resolved in the past. "
            "Use this when you need historical context about a problem."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Short description of the problem"},
                "max_results": {"type": "integer", "description": "Max results (default: 3)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_system_status",
        "description": (
            "Get the current status of a service. "
            "Use this ONLY when the ticket mentions a backend service failing or returning errors. "
            "Never use for UI or display issues."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string", "description": "Service name (auth, payments, api)"}
            },
            "required": ["service"]
        }
    }
]


def search_similar_tickets(query: str, max_results: int = 3) -> list:
    mock_tickets = [
        {"id": "TICKET-1042", "title": "Authentication service returning 500 on login", "resolution": "Database connection pool exhausted. Increased max connections.", "severity": "P1"},
        {"id": "TICKET-987", "title": "Users unable to log in after deploy", "resolution": "Bad environment variable. Rolled back.", "severity": "P1"},
        {"id": "TICKET-756", "title": "Intermittent 500 errors on auth endpoint", "resolution": "Memory leak in token validation middleware.", "severity": "P2"},
    ]
    return mock_tickets[:max_results]


def get_system_status(service: str) -> dict:
    mock_statuses = {
        "auth": {"status": "degraded", "active_incident": True, "incident_id": "INC-2024-089"},
        "payments": {"status": "operational", "active_incident": False},
        "api": {"status": "operational", "active_incident": False}
    }
    return mock_statuses.get(service, {"status": "unknown", "active_incident": False})


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "search_similar_tickets":
        result = search_similar_tickets(**tool_input)
    elif tool_name == "get_system_status":
        result = get_system_status(**tool_input)
    else:
        result = {"error": f"Tool '{tool_name}' not found"}
    return json.dumps(result)


# ─────────────────────────────────────────────
# Agente
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a senior support engineer that classifies and triages support tickets.
Use the available tools to gather context before classifying.
Always use search_similar_tickets to check historical context.
Only use get_system_status if the ticket mentions a backend service failing.

Respond ONLY with valid JSON. No additional text.
Schema:
{
  "severity": "P1" | "P2" | "P3" | "P4",
  "reason": string,
  "area": "backend" | "frontend" | "infra" | "data" | "security",
  "requires_escalation": boolean,
  "recommended_action": string
}
""".strip()


def classify_ticket(ticket: str) -> dict:
    messages = [{"role": "user", "content": f"[USER]\n{ticket}\n[/USER]"}]
    MAX_ITERATIONS = 10
    iterations = 0

    while iterations < MAX_ITERATIONS:
        iterations += 1
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            temperature=0,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            import re
            text = next(b.text for b in response.content if b.type == "text")
            match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
            if match:
                return json.loads(match.group(1).strip())
            match = re.search(r"\{[\s\S]*\}", text)
            if match:
                return json.loads(match.group(0))
            return json.loads(text.strip())

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})

    raise RuntimeError(f"Agent did not converge in {MAX_ITERATIONS} iterations")