"""Go-To-Market Analyst — distribution channels, not just SEO.

Real business channels include: PLG, sales-led enterprise, marketplaces,
partnerships, retail, app stores, community, outbound, paid ads, affiliates.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的 Go-To-Market 分析师。

# Task
识别这家公司的真实分销与获客方式。**不要默认 SaaS 套路。**

# Channel Categories (枚举，再判断该公司主用哪几个)
- PLG (产品驱动增长 — 免费试用、自助开通)
- Sales-Led (企业销售 — BDR/AE/AM)
- Marketplace (App Store, Salesforce AppExchange, AWS Marketplace, Shopify)
- Partnership (集成商、转售商、咨询公司)
- Community / Content (社区、内容营销、KOL、自媒体)
- Outbound (Cold email, LinkedIn, ABM)
- Paid Acquisition (Google/Meta/LinkedIn ads, SEO)
- Retail / Offline (实体店、经销商)
- Embedded (API/SDK 嵌入第三方产品)

# Rules
1. 必须从上面 9 类里挑出至少一个主渠道、一个次渠道。
2. 引用证据包中的招聘信息、定价页 CTA、合作伙伴页等具体信号。
3. 每个判断带 [VERIFIED:url] / [INFERRED] / [MISSING]。

# Output
- ## 主渠道 (Primary)
- ## 次渠道 (Secondary)
- ## 信号证据
- ## 渠道脆弱性 (Channel risk — 如生态寄生、流量被薅)
"""


def create_gtm_analyst(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## 证据包\n{state.get('evidence_pack', 'N/A')}\n\n"
                        f"## JTBD\n{state.get('jtbd_report', 'N/A')}\n\n"
                        "请输出 GTM 分析。"
                    )
                ),
            ]
        )
        return {"gtm_report": response.content}

    return node
