"""Run artifact writer for completed OpenBusiness analyses."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from openbusiness.claims import claim_label_policy, extract_verified_sources
from openbusiness.stages import stage_outputs


@dataclass(frozen=True)
class RunArtifactResult:
    """Paths written for a completed analysis run."""

    root_report_path: Path
    run_dir: Path
    run_report_path: Path
    stages_dir: Path
    evidence_path: Path
    sources_path: Path
    run_meta_path: Path


def slugify_company(value: str) -> str:
    """Return the stable output slug for a company name."""
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "company"


def write_run_artifacts(
    *,
    output_dir: str | Path,
    slug: str,
    final_state: dict,
    report: str,
    warnings: list[str],
    company: str,
    domain: str,
    ticker: str,
    output_language: str,
    ui_language: str,
    analysis_depth: str,
    analysis_pack: str,
    report_template: str,
) -> RunArtifactResult:
    """Write the report, stage outputs, evidence manifest, source list, and run metadata."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    root_report_path = output_path / f"{slug}_business_model.md"
    root_report_path.write_text(report, encoding="utf-8")

    run_dir = output_path / slug
    stages_dir = run_dir / "stages"
    stages_dir.mkdir(parents=True, exist_ok=True)

    stage_texts: list[str] = []
    for _, filename, content in stage_outputs(final_state):
        stage_texts.append(content)
        (stages_dir / filename).write_text(content, encoding="utf-8")

    run_report_path = run_dir / f"report.{output_language}.md"
    run_report_path.write_text(report, encoding="utf-8")

    evidence_pack = str(final_state.get("evidence_pack", ""))
    sources = extract_verified_sources(*stage_texts)

    evidence_path = run_dir / "evidence.json"
    evidence_path.write_text(
        json.dumps(
            {
                "company": company,
                "domain": domain,
                "ticker": ticker,
                "verified_sources": sources,
                "evidence_pack": evidence_pack,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    sources_markdown = "\n".join(f"- {source}" for source in sources) or "- [MISSING] No verified sources extracted."
    sources_path = run_dir / "sources.md"
    sources_path.write_text(f"# Sources\n\n{sources_markdown}\n", encoding="utf-8")

    run_meta_path = run_dir / "run.json"
    run_meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company": company,
        "domain": domain,
        "ticker": ticker,
        "output_language": output_language,
        "ui_language": ui_language,
        "analysis_depth": analysis_depth,
        "analysis_pack": analysis_pack,
        "report_template": report_template,
        "evidence_label_policy": claim_label_policy(),
        "language_warnings": warnings,
        "paths": {
            "root_report": str(root_report_path),
            "report": str(run_report_path),
            "stages": str(stages_dir),
            "evidence": str(evidence_path),
            "sources": str(sources_path),
        },
    }
    run_meta_path.write_text(json.dumps(run_meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return RunArtifactResult(
        root_report_path=root_report_path,
        run_dir=run_dir,
        run_report_path=run_report_path,
        stages_dir=stages_dir,
        evidence_path=evidence_path,
        sources_path=sources_path,
        run_meta_path=run_meta_path,
    )
