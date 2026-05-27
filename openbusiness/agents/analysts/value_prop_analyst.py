"""Value Proposition Analyst — what unique value, what 10x differentiator."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的价值主张分析师。

# Task
解释这个产品为什么能让客户改变行为，而不是只说"体验更好"。必须回答：
1. **核心价值**：这家公司给哪个客户段提供了什么不可替代或明显更优的结果？
2. **使用前后变化**：客户原来怎么做，使用后在哪些维度发生变化？
3. **10x Better 测试**：相比替代方案，速度、价格、质量、体验、集成、风险中哪几项明显更好？能否量化？
4. **取舍与阻力**：客户采用它要付出什么代价？迁移、学习、流程、合规、组织阻力在哪里？
5. **价值可持续性**：价值来自产品架构、数据、生态、品牌、流程，还是短期功能领先？

# Rules
- 引用 JTBD 报告中识别的"替代方案"作为对比基准。
- 每个论断必须带 [VERIFIED:url] / [INFERRED] / [MISSING] 标签。
- 拒绝"为用户提供更好的体验"这种空话 — 必须说清"对谁、在什么场景、好在哪个具体维度"。
- 至少给出一个"价值主张可能不成立"的反例，并说明需要什么证据验证。
- 若无法量化 10x，只能给区间或定性等级，并标明缺失数据。

# Output
Markdown。每节末尾给出 confidence 评级 (High/Medium/Low)。
"""


def create_value_prop_analyst(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "value_prop_analyst",
                    )
                ),
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
