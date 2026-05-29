"""LangGraph pipeline — evidence-driven, linear, no debate.

Flow:
  evidence_collector
   → jtbd → value_prop → gtm → unit_econ → moat
   → synthesizer (BMC)
   → stress_tester (assumption audit)
   → finalizer (user-facing report)
"""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from openbusiness.agents.analysts import (
    create_evidence_collector,
    create_finalizer,
    create_gtm_analyst,
    create_jtbd_analyst,
    create_moat_analyst,
    create_stress_tester,
    create_synthesizer,
    create_unit_econ_analyst,
    create_value_prop_analyst,
)
from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.llm_clients.factory import get_llm
from openbusiness.stages import graph_stage_pairs


PIPELINE_STAGES = graph_stage_pairs()


def build_graph(analysis_depth: str = "standard"):
    """Compile the linear evidence-driven pipeline."""
    quick_llm = get_llm("quick")  # for analysts
    deep_llm = get_llm("deep")    # for synthesis and deep-mode final reasoning
    final_llm = deep_llm if analysis_depth == "deep" else quick_llm

    evidence_node, _ = create_evidence_collector(quick_llm)
    jtbd_node = create_jtbd_analyst(quick_llm)
    value_node = create_value_prop_analyst(quick_llm)
    gtm_node = create_gtm_analyst(quick_llm)
    unit_node, _ = create_unit_econ_analyst(quick_llm)
    moat_node = create_moat_analyst(quick_llm)
    synth_node = create_synthesizer(deep_llm)
    stress_node = create_stress_tester(final_llm)
    final_node = create_finalizer(final_llm)

    graph = StateGraph(AgentState)

    graph.add_node("evidence_collector", evidence_node)
    graph.add_node("jtbd_analyst", jtbd_node)
    graph.add_node("value_prop_analyst", value_node)
    graph.add_node("gtm_analyst", gtm_node)
    graph.add_node("unit_econ_analyst", unit_node)
    graph.add_node("moat_analyst", moat_node)
    graph.add_node("synthesizer", synth_node)
    graph.add_node("stress_tester", stress_node)
    graph.add_node("finalizer", final_node)

    graph.set_entry_point("evidence_collector")
    graph.add_edge("evidence_collector", "jtbd_analyst")
    graph.add_edge("jtbd_analyst", "value_prop_analyst")
    graph.add_edge("value_prop_analyst", "gtm_analyst")
    graph.add_edge("gtm_analyst", "unit_econ_analyst")
    graph.add_edge("unit_econ_analyst", "moat_analyst")
    graph.add_edge("moat_analyst", "synthesizer")
    graph.add_edge("synthesizer", "stress_tester")
    graph.add_edge("stress_tester", "finalizer")
    graph.add_edge("finalizer", END)

    return graph.compile()
