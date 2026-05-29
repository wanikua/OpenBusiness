"""Analysis Run module for preparing and executing the OpenBusiness pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from openbusiness.artifacts import RunArtifactResult, slugify_company, write_run_artifacts
from openbusiness.language import normalize_output_language, report_language_warnings
from openbusiness.llm_clients import config
from openbusiness.profiles import (
    AnalysisPack,
    ReportTemplate,
    load_analysis_pack,
    load_report_template,
)
from openbusiness.stages import initial_stage_state

if TYPE_CHECKING:
    from openbusiness.agents.utils.agent_state import AgentState


ANALYSIS_DEPTHS = ("standard", "deep")
StageDoneCallback = Callable[[str, dict[str, Any], dict[str, Any]], None]


@dataclass(frozen=True)
class AnalysisRunRequest:
    """Input interface for one analysis run."""

    company: str
    domain: str = ""
    ticker: str = ""
    output_dir: str | Path = "output"
    output_language: str | None = None
    ui_language: str | None = None
    analysis_depth: str = "standard"
    pack_name: str = "general"
    pack_file: str | None = None
    template_name: str = "standard"
    template_file: str | None = None


@dataclass(frozen=True)
class PreparedAnalysisRun:
    """Resolved analysis run with profile context and initial graph state."""

    company: str
    domain: str
    ticker: str
    output_dir: Path
    output_language: str
    ui_language: str
    analysis_depth: str
    analysis_pack: AnalysisPack
    report_template: ReportTemplate
    slug: str
    initial_state: AgentState


@dataclass(frozen=True)
class AnalysisRunResult:
    """Completed analysis run result."""

    final_state: dict[str, Any]
    report: str
    warnings: list[str]
    artifacts: RunArtifactResult


def resolve_analysis_languages(
    output_language: str | None,
    ui_language: str | None,
) -> tuple[str, str]:
    """Resolve report and UI languages using config defaults."""
    resolved_ui_language = normalize_output_language(ui_language or config.get_ui_language())
    if output_language is None:
        output_language = config.get_output_language(default=resolved_ui_language)
    return normalize_output_language(output_language), resolved_ui_language


def default_domain(company: str) -> str:
    """Return the historical fallback domain for a company name."""
    return f"{company.lower().replace(' ', '')}.com"


def prepare_analysis_run(request: AnalysisRunRequest) -> PreparedAnalysisRun:
    """Resolve language, profiles, output path, slug, and graph state for a run."""
    company = request.company.strip()
    if not company:
        raise ValueError("Company name is required.")
    if request.analysis_depth not in ANALYSIS_DEPTHS:
        raise ValueError(f"Unsupported analysis depth: {request.analysis_depth!r}.")

    output_language, ui_language = resolve_analysis_languages(request.output_language, request.ui_language)
    analysis_pack = load_analysis_pack(request.pack_name, request.pack_file)
    report_template = load_report_template(request.template_name, request.template_file)
    domain = request.domain.strip() or default_domain(company)

    initial_state: AgentState = {
        "company_name": company,
        "domain": domain,
        "ticker": request.ticker.strip(),
        "output_language": output_language,
        "analysis_depth": request.analysis_depth,
        "analysis_pack": analysis_pack.id,
        "report_template": report_template.id,
        "pack_context": analysis_pack.to_prompt_block(),
        "template_context": report_template.to_prompt_block(),
        **initial_stage_state(),
        "messages": [],
    }

    return PreparedAnalysisRun(
        company=company,
        domain=domain,
        ticker=request.ticker.strip(),
        output_dir=Path(request.output_dir),
        output_language=output_language,
        ui_language=ui_language,
        analysis_depth=request.analysis_depth,
        analysis_pack=analysis_pack,
        report_template=report_template,
        slug=slugify_company(company),
        initial_state=initial_state,
    )


def execute_analysis_run(
    prepared: PreparedAnalysisRun,
    on_stage_done: StageDoneCallback | None = None,
) -> AnalysisRunResult:
    """Run the graph, validate final report, and persist run artifacts."""
    from openbusiness.graph.setup import build_graph

    graph = build_graph(prepared.analysis_depth)
    final_state: dict[str, Any] = dict(prepared.initial_state)

    for event in graph.stream(prepared.initial_state, stream_mode="updates"):
        for node_name, node_output in event.items():
            output = node_output if isinstance(node_output, dict) else {}
            final_state.update(output)
            if on_stage_done:
                on_stage_done(node_name, output, final_state)

    report = str(final_state.get("final_report", ""))
    if not report:
        raise RuntimeError("Pipeline completed without a final_report.")

    warnings = report_language_warnings(report, prepared.output_language)
    artifacts = write_run_artifacts(
        output_dir=prepared.output_dir,
        slug=prepared.slug,
        final_state=final_state,
        report=report,
        warnings=warnings,
        company=prepared.company,
        domain=prepared.domain,
        ticker=prepared.ticker,
        output_language=prepared.output_language,
        ui_language=prepared.ui_language,
        analysis_depth=prepared.analysis_depth,
        analysis_pack=prepared.analysis_pack.id,
        report_template=prepared.report_template.id,
    )

    return AnalysisRunResult(final_state=final_state, report=report, warnings=warnings, artifacts=artifacts)
