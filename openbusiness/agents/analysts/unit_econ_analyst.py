"""Unit Economics Analyst — runs calculator + interprets margin structure."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.agents.utils.tool_calling import invoke_with_tools
from openbusiness.language import with_output_language
from openbusiness.tools.financial_tools import calculate_unit_economics

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的单体经济分析师 (Unit Economics Analyst)。

# Task
回答：
1. **变现模式**：订阅 / 一次性 / 抽佣 / 广告 / 混合？引用定价页或财报。
2. **客单价 (ARPU)**：基于定价页或财报推算。证据包没有则标 [MISSING]。
3. **毛利率**：公开公司用 EDGAR；非公开公司参考行业基准并标 [INFERRED]。
4. **获客成本 (CAC) & 流失率 (Churn)**：通常 [MISSING]，明确标注。
5. **情景假设**：给出保守、基准、乐观三组假设，说明每组背后的证据强度。
6. **调用 `calculate_unit_economics` 工具**：用证据 + 行业基准给出 base-case 假设，跑数。
7. **敏感性分析**：指出 LTV/CAC 对 ARPU、毛利率、CAC、流失率哪个变量最敏感。
8. **健康度结论**：基于 LTV/CAC、payback、毛利结构给出定性 + 风险点。

# Rules
- 所有数字必须带来源标签。工具计算结果是 [VERIFIED:calculation]，输入假设标 [VERIFIED:url] 或 [INFERRED]。
- 拒绝拍脑袋出数 — 假设来源说不清的，直接标 [MISSING] 并跳过。
- 不要只输出一个点估计。必须说明该数字为何可能上/下浮，以及哪个数据会改变结论。
- 如果公开数据不足，用可解释的行业区间，不要伪造精确数。

# Output
Markdown。必须包含情景表、工具计算结果摘要、敏感性结论和结论反转条件。
"""

TOOLS = [calculate_unit_economics]


def create_unit_econ_analyst(llm):
    agent_llm = llm.bind_tools(TOOLS)

    def node(state: AgentState) -> dict:
        response = invoke_with_tools(
            agent_llm,
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "unit_econ_analyst",
                    )
                ),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']} (ticker={state.get('ticker', 'N/A')})\n\n"
                        f"## 证据包\n{state.get('evidence_pack', 'N/A')}\n\n"
                        f"## JTBD\n{state.get('jtbd_report', 'N/A')}\n\n"
                        f"## Value Prop\n{state.get('value_prop_report', 'N/A')}\n\n"
                        f"## GTM\n{state.get('gtm_report', 'N/A')}\n\n"
                        "请输出单体经济分析。调用 calculate_unit_economics 工具至少一次。"
                    )
                ),
            ],
            TOOLS,
        )
        return {"unit_econ_report": response.content, "messages": []}

    return node, TOOLS
