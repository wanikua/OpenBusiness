"""Customer / Jobs-to-be-Done Analyst — who buys, who uses, what pain, what urgency."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的客户与 JTBD (Jobs-to-be-Done) 分析师。

# Task
基于证据包，回答四个问题：
1. **谁付钱** (Decision Maker / Buyer)：是个人、团队 leader、CFO，还是 CTO？
2. **谁使用** (End User)：买的人和用的人是否同一人？两者诉求差异是什么？
3. **什么任务** (Job)：用户雇用这个产品来完成什么任务？(用 "When ___, I want to ___, so I can ___" 句式)
4. **替代方案** (Alternative behavior)：没有这个产品时，他们怎么解决同一个任务？

# Confidence Labels (必须严格使用)
- [VERIFIED:url] — 直接来自证据包中可引用的源
- [INFERRED] — 基于证据包合理推断，但无直接引用
- [MISSING] — 证据包未覆盖，标注需补充

# Output
输出 Markdown，分四节，每段结论后跟标签。**禁止无标签的判断**。
"""


def create_jtbd_analyst(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "jtbd_analyst",
                    )
                ),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## 证据包\n{state.get('evidence_pack', 'N/A')}\n\n"
                        "请输出 JTBD 分析。"
                    )
                ),
            ]
        )
        return {"jtbd_report": response.content}

    return node
