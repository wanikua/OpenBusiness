"""Claim label contract for evidence-aware analysis."""

from __future__ import annotations

import re


INFERRED_LABEL = "[INFERRED]"
MISSING_LABEL = "[MISSING]"
VERIFIED_LABEL = "[VERIFIED:url]"

CLAIM_LABEL_POLICY = {
    "verified": "[VERIFIED:url] means directly supported by cited source evidence.",
    "inferred": "[INFERRED] means reasoned from evidence without direct citation.",
    "missing": "[MISSING] means important data was absent or unavailable.",
}

EVIDENCE_LABEL_DISCIPLINE = """\
# Evidence Label Discipline
This is a core OpenBusiness product principle: know what is known, infer only
when the evidence supports it, and explicitly mark what is unknown.

- Preserve `[VERIFIED:url]` only for claims directly supported by source evidence.
- Use `[INFERRED]` for reasoned conclusions that depend on evidence but lack a direct citation.
- Use `[MISSING]` when important data is absent, unavailable, private, or not collected.
- Never let an analysis pack or report template remove, soften, or hide these labels.
- Do not upgrade `[INFERRED]` or `[MISSING]` claims into verified facts during synthesis.
"""

_VERIFIED_RE = re.compile(r"\[VERIFIED:([^\]]+)\]")


def verified_source_tag(url: str) -> str:
    """Return a verified source tag for a non-empty URL."""
    normalized = url.strip()
    if not normalized:
        return MISSING_LABEL
    return f"[VERIFIED:{normalized}]"


def extract_verified_sources(*texts: str) -> list[str]:
    """Extract unique verified source URLs in first-seen order."""
    sources: list[str] = []
    seen: set[str] = set()
    for text in texts:
        for source in _VERIFIED_RE.findall(text or ""):
            normalized = source.strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                sources.append(normalized)
    return sources


def claim_label_policy() -> dict[str, str]:
    """Return the stable claim label policy metadata."""
    return dict(CLAIM_LABEL_POLICY)
