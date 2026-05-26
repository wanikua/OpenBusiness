"""Conditional edge logic for the LangGraph pipeline."""

from __future__ import annotations

from openbusiness.agents.utils.agent_state import AgentState

DEFAULT_DEBATE_ROUNDS = 2


def should_continue_debate(state: AgentState) -> str:
    """Decide whether the bull/bear debate should continue or advance to judgment."""
    current_round = state.get("debate_round", 0)
    if current_round < DEFAULT_DEBATE_ROUNDS:
        return "continue_debate"
    return "end_debate"
