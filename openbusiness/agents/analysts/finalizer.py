"""Finalizer — produces the user-facing terminal report.

Combines the Canvas + Stress Test into a single Markdown document
with clean separation of facts vs assumptions vs gaps.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的报告整理员 (Finalizer)。

# Task
把上游的 Canvas 报告和 Stress Test 报告拼成最终的用户报告。**不要重写内容，只做整合与排版。**

# Output Structure (严格按此格式)

# 📊 OpenBusiness Business Model Reverse Engineering Report

**Target:** [公司名] | **Confidence:** [Robust/Plausible/Fragile/Speculative]

---

## 1. Business Model Canvas
[Canvas 报告原文]

---

## 2. Key Fact Layers
### 🟢 Verified Facts
[从 Canvas 提取所有 [VERIFIED:url] 条目]

### 🟡 Inferred Assumptions
[从 Canvas 提取所有 [INFERRED] 条目]

### 🔴 Missing Data
[从 Canvas 提取所有 [MISSING] 条目]

---

## 3. Assumption Stress Test
[Stress Test 报告原文]

---

## 4. Next Steps
Based on the analysis above, give the user 3 actionable recommendations:
- What data should be collected next to investigate this company more deeply?
- What is most worth copying if someone wanted to replicate this business model?
- What is the fatal weakness if someone wanted to enter the same market?
"""


def create_finalizer(llm):
    def node(state: AgentState) -> dict:
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
                        f"## Canvas\n{state.get('canvas_report', 'N/A')}\n\n"
                        f"## Stress Test\n{state.get('stress_test_report', 'N/A')}\n\n"
                        "请整合输出最终报告。"
                    )
                ),
            ]
        )
        return {"final_report": response.content}

    return node
