"""Finalizer — produces the user-facing terminal report.

Combines the Canvas + Stress Test into a single Markdown document
with clean separation of facts vs assumptions vs gaps.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

STANDARD_CONTEXT_CHARS = 7000
DEEP_CONTEXT_CHARS = 14000

SYSTEM_PROMPT = """\
# Role
You are the OpenBusiness Finalizer.

# Task
Assemble the upstream Canvas report and Stress Test report into one final
user-facing Markdown report. Do not invent new evidence. Only organize,
compress, localize, and lightly normalize wording when needed for language purity.

# Output Contract
Use the localized template appended below as the only output structure. It
overrides any upstream heading language. Output only the final Markdown report;
do not add an introduction, apology, explanation, or process narration.

# Content Requirements
- Include the target company and a confidence label.
- Start with a concise executive thesis. It must state the core mechanism, not just a summary.
- Include a compressed canvas report. Do not paste long upstream sections verbatim when they repeat.
- Extract and group verified facts, inferred assumptions, and missing data.
- Include a profit-engine section that explains value creation, value capture, acquisition,
  retention/expansion, margin structure, and the biggest economic sensitivity.
- Include a strategic interpretation section with the strongest insight, biggest weakness,
  likely competitor response, and what would change the conclusion.
- Include the stress test report.
- End with three actionable next steps in the requested output language:
  collect next data, identify what is worth copying, and identify the fatal
  weakness for a new entrant.
- Keep the final report dense. Prefer tables and short causal bullets over long prose.
"""


def create_finalizer(llm):
    def node(state: AgentState) -> dict:
        max_chars = DEEP_CONTEXT_CHARS if state.get("analysis_depth") == "deep" else STANDARD_CONTEXT_CHARS
        canvas_report = state.get("canvas_report", "N/A")[:max_chars]
        stress_test_report = state.get("stress_test_report", "N/A")[:max_chars]
        response = llm.invoke(
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "finalizer",
                    )
                ),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## Canvas\n{canvas_report}\n\n"
                        f"## Stress Test\n{stress_test_report}\n\n"
                        "请整合输出最终报告。"
                    )
                ),
            ]
        )
        return {"final_report": response.content}

    return node
