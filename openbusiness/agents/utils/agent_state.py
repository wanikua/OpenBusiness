"""Shared state bus for the multi-agent pipeline.

All agents read from and write to this TypedDict.
Downstream agents consume upstream reports — agents never message each other directly.
"""

from __future__ import annotations

from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Central state that flows through the entire LangGraph pipeline."""

    # ── User input ───────────────────────────────────────────────
    company_name: str
    domain: str
    ticker: str  # empty string if private company

    # ── Analyst reports (written by analyst nodes) ───────────────
    traffic_report: str
    financial_report: str
    competitive_report: str
    product_report: str

    # ── Researcher debate (optimist vs pessimist) ────────────────
    optimist_argument: str
    pessimist_argument: str
    debate_round: int

    # ── Manager synthesis ────────────────────────────────────────
    research_verdict: str  # research director's judgment
    final_report: str      # strategy director's BMC + insights

    # ── Scratch-pad messages for tool-calling agents ─────────────
    messages: Annotated[list, add_messages]
