"""Analysis packs and report templates for OpenBusiness."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

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


def _load_toml(path: Any) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _split_template_frontmatter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("+++\n"):
        raise ValueError("Template file must start with TOML front matter delimited by +++.")
    try:
        _, rest = raw.split("+++\n", 1)
        frontmatter, body = rest.split("+++\n", 1)
    except ValueError as exc:
        raise ValueError("Template file must close TOML front matter with +++.") from exc
    data = tomllib.loads(frontmatter)
    return data, body


def _path_label(path: Any) -> str:
    return str(path)


def _required_text(data: dict[str, Any], key: str, file_label: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{file_label} must define non-empty {key!r}.")
    return value.strip()


def _required_text_items(data: dict[str, Any], key: str, file_label: str) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list | tuple):
        raise ValueError(f"{file_label} must define {key!r} as a non-empty list.")
    items = tuple(str(item).strip() for item in value if str(item).strip())
    if not items:
        raise ValueError(f"{file_label} must define {key!r} as a non-empty list.")
    return items


class ProfileRegistry:
    """Loader and validator for built-in and custom profiles."""

    def __init__(self, resource_package: str = "openbusiness.resources") -> None:
        self.resource_package = resource_package

    def _resource_files(self, directory: str, suffix: str) -> list[Any]:
        base = resources.files(self.resource_package).joinpath(directory)
        return sorted(path for path in base.iterdir() if path.name.endswith(suffix))

    def load_pack_file(self, path: Any) -> AnalysisPack:
        """Load and validate a TOML analysis pack."""
        file_label = _path_label(path)
        try:
            data = _load_toml(path)
        except FileNotFoundError as exc:
            raise ValueError(f"Profile file not found: {file_label}.") from exc
        return AnalysisPack(
            id=_required_text(data, "id", file_label),
            name=_required_text(data, "name", file_label),
            description=_required_text(data, "description", file_label),
            evidence_focus=_required_text_items(data, "evidence_focus", file_label),
            analyst_focus=_required_text_items(data, "analyst_focus", file_label),
        )

    def list_analysis_packs(self) -> list[AnalysisPack]:
        """Return packaged analysis packs."""
        return [self.load_pack_file(path) for path in self._resource_files("packs", ".toml")]

    def load_analysis_pack(self, name: str = "general", file_path: str | None = None) -> AnalysisPack:
        """Load an analysis pack by packaged id or custom TOML file path."""
        if file_path:
            return self.load_pack_file(Path(file_path).expanduser())
        normalized = name.strip().lower()
        packs = self.list_analysis_packs()
        for pack in packs:
            if normalized in {pack.id.lower(), pack.name.lower()}:
                return pack
        available = ", ".join(pack.id for pack in packs)
        raise ValueError(f"Unknown analysis pack: {name!r}. Available packs: {available}.")

    def load_template_file(self, path: Any) -> ReportTemplate:
        """Load and validate a Markdown report template."""
        file_label = _path_label(path)
        try:
            data, body = _split_template_frontmatter(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"Profile file not found: {file_label}.") from exc
        body = body.strip()
        if not body:
            raise ValueError(f"{file_label} must define a non-empty template body.")
        return ReportTemplate(
            id=_required_text(data, "id", file_label),
            name=_required_text(data, "name", file_label),
            description=_required_text(data, "description", file_label),
            body=body,
        )

    def list_report_templates(self) -> list[ReportTemplate]:
        """Return packaged report templates."""
        return [self.load_template_file(path) for path in self._resource_files("templates", ".md")]

    def load_report_template(self, name: str = "standard", file_path: str | None = None) -> ReportTemplate:
        """Load a report template by packaged id or custom Markdown file path."""
        if file_path:
            return self.load_template_file(Path(file_path).expanduser())
        normalized = name.strip().lower()
        templates = self.list_report_templates()
        for template in templates:
            if normalized in {template.id.lower(), template.name.lower()}:
                return template
        available = ", ".join(template.id for template in templates)
        raise ValueError(f"Unknown report template: {name!r}. Available templates: {available}.")


DEFAULT_PROFILE_REGISTRY = ProfileRegistry()


def list_analysis_packs() -> list[AnalysisPack]:
    """Return packaged analysis packs."""
    return DEFAULT_PROFILE_REGISTRY.list_analysis_packs()


def load_analysis_pack(name: str = "general", file_path: str | None = None) -> AnalysisPack:
    """Load an analysis pack by packaged id or custom TOML file path."""
    return DEFAULT_PROFILE_REGISTRY.load_analysis_pack(name, file_path)


def list_report_templates() -> list[ReportTemplate]:
    """Return packaged report templates."""
    return DEFAULT_PROFILE_REGISTRY.list_report_templates()


def load_report_template(name: str = "standard", file_path: str | None = None) -> ReportTemplate:
    """Load a report template by packaged id or custom Markdown file path."""
    return DEFAULT_PROFILE_REGISTRY.load_report_template(name, file_path)
