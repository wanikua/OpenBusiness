"""Stage catalog for the OpenBusiness analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from openbusiness.language import normalize_output_language


@dataclass(frozen=True)
class PipelineStage:
    """One ordered LangGraph stage and its persistent output mapping."""

    node_name: str
    state_key: str
    artifact_filename: str
    english_label: str
    chinese_label: str


PIPELINE_STAGES = (
    PipelineStage("evidence_collector", "evidence_pack", "01_evidence.md", "🔍 Evidence Collector", "🔍 证据收集"),
    PipelineStage("jtbd_analyst", "jtbd_report", "02_jtbd.md", "👥 Customer / JTBD Analyst", "👥 客户与待完成任务分析"),
    PipelineStage(
        "value_prop_analyst",
        "value_prop_report",
        "03_value_prop.md",
        "💎 Value Proposition Analyst",
        "💎 价值主张分析",
    ),
    PipelineStage("gtm_analyst", "gtm_report", "04_gtm.md", "🚀 Go-To-Market Analyst", "🚀 市场进入分析"),
    PipelineStage(
        "unit_econ_analyst",
        "unit_econ_report",
        "05_unit_econ.md",
        "💰 Unit Economics Analyst",
        "💰 单体经济分析",
    ),
    PipelineStage("moat_analyst", "moat_report", "06_moat.md", "🛡️ Moat & Competition Analyst", "🛡️ 护城河与竞争分析"),
    PipelineStage("synthesizer", "canvas_report", "07_canvas.md", "🧱 Business Model Synthesizer", "🧱 商业模式合成"),
    PipelineStage(
        "stress_tester",
        "stress_test_report",
        "08_stress_test.md",
        "🔬 Assumption Stress Tester",
        "🔬 假设压力测试",
    ),
    PipelineStage("finalizer", "final_report", "09_final.md", "📝 Report Finalizer", "📝 报告整理"),
)


def graph_stage_pairs() -> list[tuple[str, str]]:
    """Return node/label pairs for graph callers that need the old shape."""
    return [(stage.node_name, stage.english_label) for stage in PIPELINE_STAGES]


def stage_labels(language: str) -> dict[str, str]:
    """Return display labels by graph node for the requested UI language."""
    normalized = normalize_output_language(language)
    return {
        stage.node_name: stage.chinese_label if normalized == "zh" else stage.english_label
        for stage in PIPELINE_STAGES
    }


def stage_artifacts() -> dict[str, str]:
    """Return output-state-key to artifact filename mapping."""
    return {stage.state_key: stage.artifact_filename for stage in PIPELINE_STAGES}


def initial_stage_state() -> dict[str, str]:
    """Return empty output slots for every pipeline stage."""
    return {stage.state_key: "" for stage in PIPELINE_STAGES}


def stage_outputs(final_state: dict) -> Iterable[tuple[str, str, str]]:
    """Yield populated stage outputs as state key, filename, content."""
    for stage in PIPELINE_STAGES:
        content = final_state.get(stage.state_key, "")
        if content:
            yield stage.state_key, stage.artifact_filename, str(content)
