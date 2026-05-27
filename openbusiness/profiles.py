"""Analysis packs and report templates for OpenBusiness."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # type: ignore


@dataclass(frozen=True)
class AnalysisPack:
    """Domain-specific analysis guidance."""

    id: str
    name: str
    description: str
    evidence_focus: tuple[str, ...]
    analyst_focus: tuple[str, ...]

    def to_prompt_block(self) -> str:
        evidence = "\n".join(f"- {item}" for item in self.evidence_focus)
        analyst = "\n".join(f"- {item}" for item in self.analyst_focus)
        return (
            f"# Analysis Pack: {self.name}\n"
            f"{self.description}\n\n"
            "## Evidence Focus\n"
            f"{evidence}\n\n"
            "## Analyst Focus\n"
            f"{analyst}"
        )


@dataclass(frozen=True)
class ReportTemplate:
    """Audience-specific report guidance."""

    id: str
    name: str
    description: str
    body: str

    def to_prompt_block(self) -> str:
        return (
            f"# Report Template: {self.name}\n"
            f"{self.description}\n\n"
            f"{self.body.strip()}"
        )


def _resource_files(directory: str, suffix: str) -> list[Path]:
    base = resources.files("openbusiness.resources").joinpath(directory)
    return sorted(path for path in base.iterdir() if path.name.endswith(suffix))


def _load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _load_pack_file(path: Path) -> AnalysisPack:
    data = _load_toml(path)
    return AnalysisPack(
        id=str(data["id"]),
        name=str(data["name"]),
        description=str(data["description"]),
        evidence_focus=tuple(str(item) for item in data.get("evidence_focus", [])),
        analyst_focus=tuple(str(item) for item in data.get("analyst_focus", [])),
    )


def list_analysis_packs() -> list[AnalysisPack]:
    """Return packaged analysis packs."""
    return [_load_pack_file(path) for path in _resource_files("packs", ".toml")]


def load_analysis_pack(name: str = "general", file_path: str | None = None) -> AnalysisPack:
    """Load an analysis pack by packaged id or custom TOML file path."""
    if file_path:
        return _load_pack_file(Path(file_path).expanduser())
    normalized = name.strip().lower()
    for pack in list_analysis_packs():
        if normalized in {pack.id.lower(), pack.name.lower()}:
            return pack
    available = ", ".join(pack.id for pack in list_analysis_packs())
    raise ValueError(f"Unknown analysis pack: {name!r}. Available packs: {available}.")


def _split_template_frontmatter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("+++\n"):
        raise ValueError("Template file must start with TOML front matter delimited by +++.")
    _, rest = raw.split("+++\n", 1)
    frontmatter, body = rest.split("+++\n", 1)
    data = tomllib.loads(frontmatter)
    return data, body


def _load_template_file(path: Path) -> ReportTemplate:
    data, body = _split_template_frontmatter(path.read_text(encoding="utf-8"))
    return ReportTemplate(
        id=str(data["id"]),
        name=str(data["name"]),
        description=str(data["description"]),
        body=body,
    )


def list_report_templates() -> list[ReportTemplate]:
    """Return packaged report templates."""
    return [_load_template_file(path) for path in _resource_files("templates", ".md")]


def load_report_template(name: str = "standard", file_path: str | None = None) -> ReportTemplate:
    """Load a report template by packaged id or custom Markdown file path."""
    if file_path:
        return _load_template_file(Path(file_path).expanduser())
    normalized = name.strip().lower()
    for template in list_report_templates():
        if normalized in {template.id.lower(), template.name.lower()}:
            return template
    available = ", ".join(template.id for template in list_report_templates())
    raise ValueError(f"Unknown report template: {name!r}. Available templates: {available}.")
