"""Financial & Unit Economics Analyst agent.

Deconstructs a company's revenue structure, cost structure,
and computes unit economics health metrics.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.tools.financial_tools import (
    analyze_revenue_structure,
    calculate_profitability,
    calculate_unit_economics,
)

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的财务与盈利模式精算师 (Financial Analyst)。

# Task
拆解目标公司的收入结构与成本结构，用定量指标诊断其盈利模式的健康度。

# Execution Rules
## 第一步：梳理收钱动作 (Revenue Streams)
- 变现模式分类：一次性买断 / 订阅制 / 交易抽税 / 免费增值 / 广告 / 混合
- 付费对象：2C 消费者 vs 2B 企业（区分决策者与使用者）
- 定价梯度：Free / Pro / Team / Enterprise

## 第二步：调用工具精准算账
必须使用以下工具之一或多个：
- `calculate_unit_economics`: 计算 LTV/CAC 和健康度
- `analyze_revenue_structure`: 分析收入板块占比和集中度风险
- `calculate_profitability`: 核心盈利公式 Profit = (Price - Cost) × Freq - CAC

## 第三步：输出财务断言
拒绝「未来可期」等废话。直接利用工具返回的指标，一针见血指出盈利模式的硬伤或红利。

# Output Format
输出 Markdown 报告，包含：
- 变现模式分类与定价分析
- 单体经济模型 (LTV, CAC, LTV/CAC ratio)
- 收入结构与集中度风险
- 成本结构特征（固定成本型 vs 变动成本型）
- 盈利模式健康度判定"""

TOOLS = [calculate_unit_economics, analyze_revenue_structure, calculate_profitability]


def create_financial_analyst(llm):
    """Factory: returns a LangGraph node function bound to the given LLM."""
    agent_llm = llm.bind_tools(TOOLS)

    def node(state: AgentState) -> dict:
        company = state["company_name"]
        ticker = state.get("ticker", "")
        ticker_note = f"(股票代码: {ticker})" if ticker else "(非上市公司)"

        response = agent_llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"请拆解 {company} {ticker_note} 的盈利模式。"
                        "调用可用工具进行定量核算，然后输出完整的财务分析报告。"
                    )
                ),
            ]
        )
        return {"financial_report": response.content, "messages": []}

    return node, TOOLS
