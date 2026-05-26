"""LangGraph pipeline setup — wires all agents into a StateGraph.

Pipeline flow:
  1. [Parallel] 4 Analysts → produce domain reports
  2. [Loop]     Optimist ↔ Pessimist debate (N rounds)
  3.            Research Director → judgment
  4.            Strategy Director → final BMC report
"""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from openbusiness.agents.analysts.competitive_analyst import create_competitive_analyst
from openbusiness.agents.analysts.financial_analyst import create_financial_analyst
from openbusiness.agents.analysts.product_analyst import create_product_analyst
from openbusiness.agents.analysts.traffic_analyst import create_traffic_analyst
from openbusiness.agents.managers.research_director import create_research_director
from openbusiness.agents.managers.strategy_director import create_strategy_director
from openbusiness.agents.researchers.optimist import create_optimist_researcher
from openbusiness.agents.researchers.pessimist import create_pessimist_researcher
from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.graph.conditional_logic import should_continue_debate
from openbusiness.llm_clients.factory import get_llm


def build_graph(debate_rounds: int = 2):
    """Construct and compile the full analysis pipeline.

    Args:
        debate_rounds: Number of bull/bear debate rounds.

    Returns:
        A compiled LangGraph that can be invoked with an AgentState dict.
    """
    quick_llm = get_llm("quick")
    deep_llm = get_llm("deep")

    # ── Create agent nodes ───────────────────────────────────────
    traffic_node, _ = create_traffic_analyst(quick_llm)
    financial_node, _ = create_financial_analyst(quick_llm)
    competitive_node, _ = create_competitive_analyst(quick_llm)
    product_node, _ = create_product_analyst(quick_llm)

    optimist_node = create_optimist_researcher(quick_llm)
    pessimist_node = create_pessimist_researcher(quick_llm)

    research_director_node = create_research_director(deep_llm)
    strategy_director_node = create_strategy_director(deep_llm)

    # ── Build the graph ──────────────────────────────────────────
    graph = StateGraph(AgentState)

    # Phase 1: Analysts (sequential — each writes to its own state field)
    graph.add_node("traffic_analyst", traffic_node)
    graph.add_node("financial_analyst", financial_node)
    graph.add_node("competitive_analyst", competitive_node)
    graph.add_node("product_analyst", product_node)

    # Phase 2: Bull/Bear debate
    graph.add_node("optimist", optimist_node)
    graph.add_node("pessimist", pessimist_node)

    # Phase 3: Managers
    graph.add_node("research_director", research_director_node)
    graph.add_node("strategy_director", strategy_director_node)

    # ── Wire edges ───────────────────────────────────────────────

    # Analysts run sequentially (each reads only its own input, writes its own field)
    graph.set_entry_point("traffic_analyst")
    graph.add_edge("traffic_analyst", "financial_analyst")
    graph.add_edge("financial_analyst", "competitive_analyst")
    graph.add_edge("competitive_analyst", "product_analyst")

    # After all analysts → start debate
    graph.add_edge("product_analyst", "optimist")

    # Debate loop: optimist → pessimist → check round count
    graph.add_edge("optimist", "pessimist")
    graph.add_conditional_edges(
        "pessimist",
        should_continue_debate,
        {
            "continue_debate": "optimist",
            "end_debate": "research_director",
        },
    )

    # Managers: research director → strategy director → END
    graph.add_edge("research_director", "strategy_director")
    graph.add_edge("strategy_director", END)

    return graph.compile()
