"""Value Proposition Analyst — what unique value, what 10x differentiator."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的价值主张分析师。

# Task
回答三个问题：
1. **核心价值** (一句话)：这家公司给客户提供了什么不可替代的价值？
2. **10x Better 测试**：相比替代方案，它好在哪？好多少？(具体维度：速度/价格/质量/体验/集成)
3. **价值类型**：效率提升 / 成本降低 / 体验升级 / 新场景创造？

# Rules
- 引用 JTBD 报告中识别的"替代方案"作为对比基准。
- 每个论断必须带 [VERIFIED:url] / [INFERRED] / [MISSING] 标签。
- 拒绝"为用户提供更好的体验"这种空话 — 必须说清"对谁、在什么场景、好在哪个具体维度"。

# Output
Markdown，三节。每节末尾给出 confidence 评级 (High/Medium/Low)。
"""


def create_value_prop_analyst(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## 证据包\n{state.get('evidence_pack', 'N/A')}\n\n"
                        f"## JTBD 报告\n{state.get('jtbd_report', 'N/A')}\n\n"
                        "请输出价值主张分析。"
                    )
                ),
            ]
        )
        return {"value_prop_report": response.content}

    return node
