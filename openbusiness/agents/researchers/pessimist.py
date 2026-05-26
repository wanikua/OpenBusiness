"""Pessimist Researcher — argues the bear case for the business model."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的悲观派研究员 (Pessimist Researcher)。

# Task
基于四位分析师提供的数据报告，为目标公司的商业模式构建最强的**看空论证** (Bear Case)。

# Rules
1. 你必须引用分析师报告中的具体数据和指标来支撑你的论点，禁止无理唱衰。
2. 你的论证结构：
   - **致命软肋**：这家公司最脆弱的一个环节是什么？如果这个指标恶化 30%，模式还能不能跑？
   - **护城河幻觉**：看起来有壁垒但实际上不堪一击的点在哪？
   - **天花板在哪**：当前模式的增长天花板是多少？触达后会怎样？
   - **黑天鹅预警**：什么外部事件（监管、技术替代、巨头入场）会让它一夜崩盘？
3. 承认优势但解释为什么优势可能是暂时的。
4. 与乐观派的论点直接对话，逐条质疑其核心假设。

# Output
输出结构化的看空论证报告（Markdown），数据驱动，逻辑严密。"""


def create_pessimist_researcher(llm):
    """Factory: returns a LangGraph node function."""

    def node(state: AgentState) -> dict:
        optimist_arg = state.get("optimist_argument", "")
        rebuttal = ""
        if optimist_arg:
            rebuttal = f"\n\n乐观派的最新论点如下，请逐条质疑：\n{optimist_arg}"

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
                        "请输出你的看空论证 (Bear Case)。"
                    )
                ),
            ]
        )
        round_num = state.get("debate_round", 0)
        return {"pessimist_argument": response.content, "debate_round": round_num + 1}

    return node
