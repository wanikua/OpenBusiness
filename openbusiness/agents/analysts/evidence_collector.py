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
3. 客户案例、客户 logo、用户评价、G2/Capterra/Reddit/论坛讨论
4. 招聘页、销售岗位、客户成功岗位、解决方案工程岗位，用来判断销售动作
5. 集成、API、文档、市场、合作伙伴页，用来判断生态位置
6. 最近一年的新闻、博客、产品发布、融资或战略更新
7. 创始人/产品采访 (tavily_search "founder interview product strategy")
8. 公开财务 (sec_edgar_company_facts — 仅当 ticker 不为空时)
9. 竞品列表、替代方案、竞品定价、迁移对比页

# Rules
- 每条事实必须保留 [VERIFIED:<url>] 标签。
- 工具不可用 / API key 缺失时，**不要编造**。直接在输出中标注 [MISSING:<原因>]。
- 不要写"我认为/可能/大概"。这一层只搬运事实。
- 不只收集"公司说自己是什么"，也要收集市场、客户、招聘、竞品给出的外部信号。
- 每条关键事实后写一句"业务信号"，只说明它会帮助下游判断什么，不做最终结论。

# Output
输出一份结构化 Markdown 证据包。每条证据尽量包含：事实、来源、业务信号、可靠性。
"""

TOOLS = [tavily_search, firecrawl_scrape, sec_edgar_company_facts]


def create_evidence_collector(llm):
    agent_llm = llm.bind_tools(TOOLS)

    def node(state: AgentState) -> dict:
        ticker_note = f", ticker={state['ticker']}" if state.get("ticker") else " (private company)"
        deep_mode = state.get("analysis_depth") == "deep"
        if deep_mode:
            depth_note = (
                "深度模式：使用 search_depth='advanced' 做更广证据采集；优先补客户案例、"
                "招聘、生态、竞品定价和反面评价。"
            )
            collection_scope = (
                "至少尝试官网、定价、客户案例/评价、招聘/销售岗位、集成/生态、近期新闻、"
                "创始人采访、竞品/替代方案这些方向。"
            )
            max_rounds = 6
        else:
            depth_note = (
                "标准模式：只采集最高信号来源；优先官网、定价、客户证据、竞品/替代方案和最近新闻。"
            )
            collection_scope = "不要追求覆盖所有方向；缺失的次要方向直接标 [MISSING]。"
            max_rounds = 3
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
                        f"{depth_note}"
                        "请使用工具采集证据。"
                        f"{collection_scope}"
                        "输出完整的证据包 Markdown。"
                    )
                ),
            ],
            TOOLS,
            max_rounds=max_rounds,
        )
        return {"evidence_pack": response.content, "messages": []}

    return node, TOOLS
