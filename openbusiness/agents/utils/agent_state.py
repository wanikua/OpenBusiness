"""Shared state bus for the evidence-driven business model reconstruction pipeline.

Reports must label every finding with: [VERIFIED:url] (cited), [INFERRED] (LLM deduction),
or [MISSING] (data gap). The Synthesizer separates these in the final report.
"""

from __future__ import annotations

from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Linear evidence pipeline. No debate. No judgment loop."""

    company_name: str
    domain: str
    ticker: str
    output_language: str       # Report language: "zh" or "en"

    evidence_pack: str        # Markdown bundle: pricing, filings, news, scraped snippets

    jtbd_report: str          # Customer & Jobs-to-be-Done
    value_prop_report: str    # Value Proposition
    gtm_report: str           # Go-To-Market / Channels
    unit_econ_report: str     # Unit Economics
    moat_report: str          # Moat & Competition

    canvas_report: str        # Business Model Canvas synthesis
    stress_test_report: str   # Assumption stress test

    final_report: str

    messages: Annotated[list, add_messages]
