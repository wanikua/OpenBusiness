"""Product & Value Proposition Analyst agent.

Deconstructs what value the company creates, for whom,
and what makes it irreplaceable (or not).
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.tools.web_tools import fetch_company_overview, fetch_pricing_page

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的产品与价值主张分析师 (Product Analyst)。

# Task
拆解目标公司的核心价值主张：它为谁解决了什么不可替代的痛点？

# Analysis Framework

## 1. 客户细分 (Customer Segments)
- 核心买单客户是谁？（2B: 区分决策者 vs 使用者）
- 用户画像：规模、行业、场景
- 付费意愿驱动力：省钱？省时？情绪价值？身份认同？

## 2. 价值主张 (Value Proposition)
- 核心痛点：用一句话说清它解决了什么问题
- 价值类型：效率提升 / 成本降低 / 体验升级 / 新场景创造
- 「10x better」测试：相比替代方案，它好在哪？好多少？

## 3. 客户关系 (Customer Relationships)
- 留存机制：社区 / 数据锁定 / 习惯养成 / 合同周期
- 推荐机制：口碑传播 / 邀请激励 / 内容模板生态

## 4. 核心资源与关键业务 (Key Resources & Activities)
- 护城河资产：算法 / 数据 / 品牌 / 网络效应 / 专利
- 每天在忙什么：研发驱动 / 运营驱动 / 营销驱动

# Output
输出产品分析报告，重点阐述价值主张和护城河评估。"""

TOOLS = [fetch_company_overview, fetch_pricing_page]


def create_product_analyst(llm):
    """Factory: returns a LangGraph node function bound to the given LLM."""
    agent_llm = llm.bind_tools(TOOLS)

    def node(state: AgentState) -> dict:
        company = state["company_name"]
        domain = state["domain"]

        response = agent_llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"请拆解 {company} (域名: {domain}) 的产品与价值主张。"
                        "调用可用工具获取基础数据后，输出完整的产品分析报告。"
                    )
                ),
            ]
        )
        return {"product_report": response.content, "messages": []}

    return node, TOOLS
