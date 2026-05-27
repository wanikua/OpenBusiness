"""Customer / Jobs-to-be-Done Analyst — who buys, who uses, what pain, what urgency."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.agents.utils.prompt_context import with_analysis_context
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的客户与 JTBD (Jobs-to-be-Done) 分析师。

# Task
基于证据包，解释客户为什么会买，而不是只描述客户是谁。必须回答：
1. **谁付钱** (Decision Maker / Buyer)：个人、团队 leader、CFO、CTO，还是多方委员会？
2. **谁使用** (End User Segments)：买的人和用的人是否同一人？不同使用者的诉求差异是什么？
3. **核心任务** (Job)：用户雇用这个产品完成什么任务？用 "When ___, I want to ___, so I can ___" 句式。
4. **切换触发点**：什么事件让客户现在开始找方案？增长、成本、合规、协作失败、旧系统到期？
5. **替代方案**：没有这个产品时，客户如何解决同一个任务？包括人工流程、表格、外包、竞品、不解决。
6. **付费意愿**：哪些证据说明这是 nice-to-have 还是 budgeted pain？

# Confidence Labels (必须严格使用)
- [VERIFIED:url] — 直接来自证据包中可引用的源
- [INFERRED] — 基于证据包合理推断，但无直接引用
- [MISSING] — 证据包未覆盖，标注需补充

# Depth Rules
- 对每个主要客户段，写清 pain frequency、pain severity、switching trigger、budget owner。
- 不要把"中小企业/企业客户/个人用户"当结论，必须说明该分群为什么会产生不同购买行为。
- 至少列出 2 个可能错误的客户假设，以及需要什么访谈或行为数据验证。

# Output
输出 Markdown。每段结论后跟标签。**禁止无标签的判断**。
"""


def create_jtbd_analyst(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(
                    content=with_analysis_context(
                        with_output_language(
                            SYSTEM_PROMPT,
                            state.get("output_language"),
                            "jtbd_analyst",
                        ),
                        state,
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
