"""Small helper for models that return tool calls without executing them."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from collections.abc import Sequence
from typing import Any

from langchain_core.messages import HumanMessage, ToolMessage


def invoke_with_tools(llm, messages: list, tools: Sequence, max_rounds: int = 4):
    """Invoke an LLM and execute any returned LangChain tool calls.

    `bind_tools()` exposes tool schemas to the model, but it does not execute
    returned calls. This helper runs the calls, appends ToolMessage results, and
    asks the model to continue until it returns normal content.
    """
    tools_by_name = {tool.name: tool for tool in tools}
    response = llm.invoke(messages)

    def run_tool_call(call: dict[str, Any]) -> ToolMessage:
        name = call.get("name")
        args: dict[str, Any] = call.get("args") or {}
        tool_call_id = call.get("id")
        tool = tools_by_name.get(name)

        if tool is None:
            result = json.dumps({"error": f"Unknown tool: {name}"}, ensure_ascii=False)
        else:
            try:
                result = tool.invoke(args)
            except Exception as exc:
                result = json.dumps({"error": str(exc), "tool": name}, ensure_ascii=False)

        return ToolMessage(content=str(result), tool_call_id=tool_call_id)

    for _ in range(max_rounds):
        tool_calls = getattr(response, "tool_calls", None) or []
        if not tool_calls:
            return response

        with ThreadPoolExecutor(max_workers=min(len(tool_calls), 6)) as executor:
            tool_messages = list(executor.map(run_tool_call, tool_calls))

        messages = [
            *messages,
            response,
            *tool_messages,
            HumanMessage(
                content=(
                    "Using the tool results above, produce only the requested final Markdown. "
                    "Do not narrate tool usage or describe what you are about to do."
                )
            ),
        ]
        response = llm.invoke(messages)

    return response
