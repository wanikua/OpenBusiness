"""Go-To-Market Analyst — distribution channels, not just SEO.

Real business channels include: PLG, sales-led enterprise, marketplaces,
partnerships, retail, app stores, community, outbound, paid ads, affiliates.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState
from openbusiness.language import with_output_language

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的 Go-To-Market 分析师。

# Task
识别这家公司的真实分销、销售动作和增长机制。**不要默认 SaaS 套路。**

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
4. 区分早期获客渠道、规模化渠道和留存/扩张渠道。
5. 对每个主渠道说明：目标客户、触达方式、转化摩擦、成本结构、可扩展性、被竞争对手复制的难度。
6. 至少写一个增长飞轮假设，以及一个会让该飞轮失效的条件。

# Output
Markdown。避免只列渠道名称，必须解释渠道为什么适合该客户任务和价格带。
"""


def create_gtm_analyst(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(
                    content=with_output_language(
                        SYSTEM_PROMPT,
                        state.get("output_language"),
                        "gtm_analyst",
                    )
                ),
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
