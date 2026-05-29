"""Structured result helpers for evidence collection tools."""

from __future__ import annotations

import json
from typing import Any

from openbusiness.claims import verified_source_tag


def json_result(payload: dict[str, Any]) -> str:
    """Return deterministic JSON for tool results."""
    return json.dumps(payload, ensure_ascii=False)


def missing_result(tool: str, warning: str, fallback_action: str, **extra: Any) -> str:
    """Return a missing-data result with explicit caller guidance."""
    payload: dict[str, Any] = {
        "tool": tool,
        "status": "missing",
        "warning": warning,
        "fallback_action": fallback_action,
    }
    payload.update(extra)
    return json_result(payload)


def error_result(tool: str, error: str, **extra: Any) -> str:
    """Return a recoverable tool error result."""
    payload: dict[str, Any] = {"tool": tool, "status": "error", "error": error}
    payload.update(extra)
    return json_result(payload)


def verified_result(tool: str, **extra: Any) -> str:
    """Return a verified tool result."""
    payload: dict[str, Any] = {"tool": tool, "status": "verified"}
    payload.update(extra)
    return json_result(payload)


def source_tag(url: str) -> str:
    """Return the claim-contract source tag for a URL."""
    return verified_source_tag(url)
