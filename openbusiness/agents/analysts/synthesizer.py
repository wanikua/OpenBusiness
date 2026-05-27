"""Business Model Synthesizer — assembles the BMC from all upstream reports.

Output structure separates VERIFIED facts, INFERRED assumptions, and MISSING data.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
You are the OpenBusiness Business Model Synthesizer.

# Task
Combine the upstream analyst reports (JTBD, Value Prop, GTM, Unit Econ, Moat)
into one structured business model canvas.

# Critical Rule — Tag Preservation
Every canvas cell must preserve upstream [VERIFIED:url], [INFERRED], and
[MISSING] tags. The synthesis must not flatten evidence quality.

# Output Contract
Use the localized template appended below as the only output structure. Translate
upstream headings and prose into the requested output language before writing the
final Markdown. Output only the canvas report; do not add an introduction,
apology, explanation, or process narration.

# Content Requirements
- Include the business model canvas tables.
- Open with a strategic thesis that explains what the business really is, how it captures value,
  and what has to remain true for it to keep working.
- Include an at-a-glance judgment table for non-specialist readers. It must answer:
  customer, buyer, end user, ToB/ToC/B2B2C classification, revenue model,
  current stage, growth outlook, major investors/funding, and one-sentence risk.
- The at-a-glance table must use explicit classifications, not prose-only labels:
  funding stage must be one of Pre-Seed, Seed, Series A, Series B, Series C+, Growth,
  Public, Bootstrapped, No announced financing plan, or Not found; moat verdict must be
  Strong, Moderate, Weak, or None; outlook must be Strong, Positive, Mixed, Weak, or Unknown.
  If the requested classification cannot be supported, write Not found or Unknown with [MISSING].
- Include a unit economics snapshot and moat snapshot.
- Explain the profit engine: who pays, why they pay, how the company acquires them,
  where gross margin comes from, and what drives expansion or churn.
- Include funding and investor signals. If funding data is missing, explicitly mark it [MISSING]
  instead of omitting the topic.
- Include a causal chain from customer pain to value proposition to channel to monetization to moat.
- Include 2-3 non-obvious insights. Each insight must say why it matters and what could make it wrong.
- List verified facts, inferred assumptions, and missing data separately.
- Keep company names, URLs, metric abbreviations, and evidence tags unchanged.
- Keep the synthesis dense. Do not repeat the same point across multiple sections.
"""


def create_synthesizer(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "synthesizer",
                    )
                ),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## JTBD\n{state.get('jtbd_report', 'N/A')}\n\n"
                        f"## Value Prop\n{state.get('value_prop_report', 'N/A')}\n\n"
                        f"## GTM\n{state.get('gtm_report', 'N/A')}\n\n"
                        f"## Unit Econ\n{state.get('unit_econ_report', 'N/A')}\n\n"
                        f"## Moat\n{state.get('moat_report', 'N/A')}\n\n"
                        "请合成完整的商业模式画布报告。"
                    )
                ),
            ]
        )
        return {"canvas_report": response.content}

    return node
