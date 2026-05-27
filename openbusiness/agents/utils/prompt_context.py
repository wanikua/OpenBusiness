"""Prompt context helpers shared by analyst nodes."""

from __future__ import annotations

from openbusiness.agents.utils.agent_state import AgentState


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


def analysis_context_block(state: AgentState) -> str:
    """Return evidence discipline plus optional pack/template guidance."""
    sections = [EVIDENCE_LABEL_DISCIPLINE]
    pack_context = state.get("pack_context")
    if pack_context:
        sections.append(pack_context)
    template_context = state.get("template_context")
    if template_context:
        sections.append(template_context)
    sections.append(
        "# Context Boundary\n"
        "The pack and template guidance above changes analysis focus only. "
        f"The final output language remains `{state.get('output_language', 'zh')}`. "
        "Do not copy these system headings into the user-facing report."
    )
    return "\n\n".join(section.strip() for section in sections if section.strip())


def with_analysis_context(system_prompt: str, state: AgentState) -> str:
    """Append shared evidence, pack, and template context to a system prompt."""
    return f"{system_prompt.rstrip()}\n\n{analysis_context_block(state)}"
