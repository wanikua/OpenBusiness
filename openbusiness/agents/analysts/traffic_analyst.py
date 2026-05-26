"""Traffic & Channel Analyst agent.

Analyzes how a company acquires users: SEO, paid ads, social, direct.
Diagnoses the health and sustainability of its acquisition funnel.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.tools.traffic_tools import analyze_seo_moat, analyze_traffic_channels

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的流量与渠道分析师 (Traffic Analyst)。

# Task
分析目标公司的用户获取渠道，诊断其流量结构的健康度与可持续性。

# Execution Rules
1. 基于已知信息，评估该公司的流量来源分布（直接访问、自然搜索、付费投放、社交/推荐、邮件）。
2. 调用 `analyze_traffic_channels` 工具进行定量诊断。
3. 如有 SEO 相关数据，调用 `analyze_seo_moat` 评估搜索护城河。
4. 最终输出必须包含：
   - 流量渠道分布（百分比）
   - 增长模型分类（PLG / 烧钱买量 / 社区驱动 / 混合）
   - 获客风险评级
   - 渠道护城河分析

# Output
输出纯文本分析报告，使用 Markdown 格式，数据尽量精确。"""

TOOLS = [analyze_traffic_channels, analyze_seo_moat]


def create_traffic_analyst(llm):
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
                        f"请分析 {company} (域名: {domain}) 的流量获取渠道与增长模型。"
                        "调用可用工具进行定量分析，然后输出完整报告。"
                    )
                ),
            ]
        )
        return {"traffic_report": response.content, "messages": []}

    return node, TOOLS
