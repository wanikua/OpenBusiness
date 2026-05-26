"""Competitive Landscape Analyst agent.

Maps the competitive environment: direct competitors, substitute products,
supplier power, buyer power, and threat of new entrants (Porter's Five Forces).
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.tools.web_tools import fetch_company_overview

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的竞争格局分析师 (Competitive Analyst)。

# Task
用波特五力模型 (Porter's Five Forces) 拆解目标公司所处的竞争环境，
评估其市场地位和战略生态位。

# Analysis Framework
1. **行业竞争强度** (Industry Rivalry)
   - 主要直接竞品是谁？市场集中度如何？
   - 竞争维度：价格战 / 产品差异化 / 品牌心智 / 生态锁定

2. **新进入者威胁** (Threat of New Entrants)
   - 进入壁垒高低：技术门槛 / 资金门槛 / 网络效应 / 监管牌照
   - 最可能的颠覆者画像

3. **替代品威胁** (Threat of Substitutes)
   - 用户还能用什么方式解决同一个痛点？
   - 替代品的转换成本有多高？

4. **供应商议价能力** (Supplier Power)
   - 核心供应商是谁？（技术栈、基础设施、内容供给方）
   - 是否存在「生态寄生风险」？（如严重依赖 OpenAI API / AWS）

5. **买家议价能力** (Buyer Power)
   - 客户集中度：是长尾小客户还是少数大客户？
   - 转换成本对买家来说有多高？

# Output
输出波特五力分析表 + 综合竞争地位评级 (Strong / Moderate / Weak)。"""

TOOLS = [fetch_company_overview]


def create_competitive_analyst(llm):
    """Factory: returns a LangGraph node function bound to the given LLM."""
    agent_llm = llm.bind_tools(TOOLS)

    def node(state: AgentState) -> dict:
        company = state["company_name"]

        response = agent_llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"请用波特五力模型分析 {company} 的竞争格局。"
                        "调用 fetch_company_overview 获取基础信息后，输出完整分析报告。"
                    )
                ),
            ]
        )
        return {"competitive_report": response.content, "messages": []}

    return node, TOOLS
