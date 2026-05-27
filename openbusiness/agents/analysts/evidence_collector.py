"""Evidence Collector — runs first. Gathers raw facts before any analysis happens."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.tools.evidence_tools import (
    firecrawl_scrape,
    sec_edgar_company_facts,
    tavily_search,
)
from openbusiness.agents.utils.tool_calling import invoke_with_tools
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的证据收集员 (Evidence Collector)。你是整条流水线的第一站，下游所有 Agent 都依赖你给出的事实底料。

# Task
为目标公司收集真实、可引用的事实。**不做分析、不下结论。**

# Required Coverage
针对目标公司，尽量收集以下原始证据：
1. 公司官网首页 (firecrawl_scrape)
2. 定价页 (firecrawl_scrape — 找 /pricing /plans /enterprise)
3. 最近一年的新闻或博客 (tavily_search "company news 2025")
4. 创始人/产品采访 (tavily_search "founder interview product strategy")
5. 公开财务 (sec_edgar_company_facts — 仅当 ticker 不为空时)
6. 竞品列表 (tavily_search "alternatives to <company>")

# Rules
- 每条事实必须保留 [VERIFIED:<url>] 标签。
- 工具不可用 / API key 缺失时，**不要编造**。直接在输出中标注 [MISSING:<原因>]。
- 不要写"我认为/可能/大概"。这一层只搬运事实。

# Output
输出一份结构化的 Markdown 证据包，分节：
- ## Website & Product Facts
- ## Pricing & Business Model Signals
- ## News & Strategy Updates
- ## Founder / Product Philosophy
- ## Financial Facts (Public Companies)
- ## Competitive Landscape
- ## Missing Data
"""

TOOLS = [tavily_search, firecrawl_scrape, sec_edgar_company_facts]


def create_evidence_collector(llm):
    agent_llm = llm.bind_tools(TOOLS)

    def node(state: AgentState) -> dict:
        ticker_note = f", ticker={state['ticker']}" if state.get("ticker") else " (private company)"
        response = invoke_with_tools(
            agent_llm,
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "evidence_collector",
                    )
                ),
                HumanMessage(
                    content=(
                        f"目标: {state['company_name']} (domain={state['domain']}{ticker_note})。"
                        "请使用工具采集证据，输出完整的证据包 Markdown。"
                    )
                ),
            ],
            TOOLS,
        )
        return {"evidence_pack": response.content, "messages": []}

    return node, TOOLS
