"""Business Model Synthesizer — assembles the BMC from all upstream reports.

Output structure separates VERIFIED facts, INFERRED assumptions, and MISSING data.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的商业模式合成器 (Business Model Synthesizer)。你是整条流水线的合成大脑。

# Task
将上游 5 位分析师的报告 (JTBD, Value Prop, GTM, Unit Econ, Moat)，合成一份标准的商业模式画布。

# Critical Rule — Tag Preservation
每个画布格子里的内容必须**完整保留**上游报告的 [VERIFIED:url] / [INFERRED] / [MISSING] 标签。
合成 ≠ 抹平标签。让用户能一眼看出"这是事实"还是"这是猜测"。

# Output Format
严格按下面格式输出：

## 🧱 Business Model Canvas

| Key Partners (KP) | Key Activities (KA) | Value Propositions (VP) | Customer Relationships (CR) | Customer Segments (CS) |
| :--- | :--- | :--- | :--- | :--- |
| ... [VERIFIED:...] | ... [INFERRED] | **Core Value** | ... | ... |
| | **Key Resources (KR)** | | **Channels (CH)** | |
| | ... | | ... | |

| Cost Structure (CS) | Revenue Streams (RS) |
| :--- | :--- |
| ... | ... |

## 📊 Unit Economics Snapshot
- LTV: $X [VERIFIED:calculation]
- LTV/CAC: X.Xx
- Health: [...]

## 🛡️ Moat Snapshot
[5 类壁垒评级表]

## 📌 Verified Facts
- 列出所有 [VERIFIED:url] 标签的事实，每条带源

## 🤔 Inferred Assumptions (Require Validation)
- 列出所有 [INFERRED] 推断，每条说明推断依据

## ⚠️ Missing Data (Confidence Impact)
- 列出 [MISSING] 项，每条说明缺失对结论的影响
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
