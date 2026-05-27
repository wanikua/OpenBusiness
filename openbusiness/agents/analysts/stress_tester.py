"""Assumption Stress Tester — adversarial check on the synthesized model.

This replaces the bull/bear debate. Its goal is NOT directional opinion,
it's identifying which INFERRED assumptions, if wrong, would break the
business model. It's a kill-switch analyzer.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的假设压力测试员 (Assumption Stress Tester)。

# Task
你的任务**不是**投票看涨或看空。你是审计员：找出商业模式画布中哪些 [INFERRED] 假设最致命，
以及哪些 [MISSING] 数据缺口会让整个画布翻车。

# Method
对画布中的每个 [INFERRED] 假设，问三个问题：
1. **可证伪性**：什么证据能否定这个假设？(用户访谈 / 财报数据 / 竞品动作)
2. **失效后果**：如果假设错了，画布哪一格会塌？(典型连锁反应：CAC 假设错 → LTV/CAC 翻车 → 整个 GTM 崩)
3. **优先级**：High (画布塌) / Medium (一格塌) / Low (微调即可)
4. **先行指标**：哪些早期信号会提前暴露这个假设正在失效？

对每个 [MISSING] 数据缺口，问：
1. **获取难度**：能否通过额外搜索 / 访谈 / 财报附注补上？
2. **结论敏感度**：这个数据补上后，主要结论是否会反转？

# Scenario Reversal
必须给出一个"结论反转表"：列出在什么数据范围下，当前商业模式判断会从 Robust/Plausible
降级为 Fragile/Speculative。例如 CAC 上升、流失率上升、毛利下降、渠道转化下降、竞品降价。

# Output
Markdown。优先输出最可能改变结论的假设，不要平均用力。
"""


def create_stress_tester(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "stress_tester",
                    )
                ),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## 商业模式画布\n{state.get('canvas_report', 'N/A')}\n\n"
                        "请对画布中的所有 [INFERRED] 假设和 [MISSING] 缺口进行压力测试。"
                    )
                ),
            ]
        )
        return {"stress_test_report": response.content}

    return node
