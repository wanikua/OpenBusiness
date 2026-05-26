"""Optimist Researcher — argues the bull case for the business model."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的乐观派研究员 (Optimist Researcher)。

# Task
基于四位分析师提供的数据报告，为目标公司的商业模式构建最强的**看多论证** (Bull Case)。

# Rules
1. 你必须引用分析师报告中的具体数据和指标来支撑你的论点，禁止空洞吹捧。
2. 你的论证结构：
   - **增长引擎**：这家公司最强的增长飞轮是什么？数据如何支撑？
   - **护城河深度**：它的壁垒到底有多深？竞争对手需要多少年/多少资金才能追上？
   - **规模化潜力**：当前模式能否 10x 放大？边际成本如何变化？
   - **估值逻辑**：以当前增速和单体经济指标，它值多少钱？
3. 承认风险但解释为什么风险可控。
4. 与悲观派的反驳直接对话，逐条反驳其核心担忧。

# Output
输出结构化的看多论证报告（Markdown），数据驱动，逻辑严密。"""


def create_optimist_researcher(llm):
    """Factory: returns a LangGraph node function."""

    def node(state: AgentState) -> dict:
        pessimist_arg = state.get("pessimist_argument", "")
        rebuttal = ""
        if pessimist_arg:
            rebuttal = f"\n\n悲观派的最新论点如下，请逐条反驳：\n{pessimist_arg}"

        response = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## 流量分析报告\n{state.get('traffic_report', 'N/A')}\n\n"
                        f"## 财务分析报告\n{state.get('financial_report', 'N/A')}\n\n"
                        f"## 竞争分析报告\n{state.get('competitive_report', 'N/A')}\n\n"
                        f"## 产品分析报告\n{state.get('product_report', 'N/A')}"
                        f"{rebuttal}\n\n"
                        "请输出你的看多论证 (Bull Case)。"
                    )
                ),
            ]
        )
        return {"optimist_argument": response.content}

    return node
