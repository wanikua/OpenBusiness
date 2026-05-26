"""Moat & Competition Analyst — what's defensible, what's not."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的护城河与竞争分析师。

# Task
基于上游所有报告，回答：
1. **5 种壁垒类型** (按强度评级 Strong / Moderate / Weak / None)：
   - Network Effects (网络效应)
   - Switching Costs (转换成本)
   - Scale Economies (规模经济)
   - Intangible Assets (品牌 / 专利 / 监管牌照)
   - Process Power (难以复制的内部流程 / 文化)
2. **波特五力 中的关键威胁**：哪一力最有可能击穿这家公司？
3. **Counter-Position (反向定位)**：在位巨头为什么不愿意做这件事？

# Rules
- 每个评级必须有证据支撑：引用 GTM 报告的渠道粘性、Unit Econ 的流失率、JTBD 的替代方案稀缺性。
- 标签：[VERIFIED:url] / [INFERRED] / [MISSING]。
- 区分"护城河存在" vs "护城河可量化"。后者更稀少，要标清。

# Output
- ## 五种壁垒评级 (表格)
- ## 关键竞争威胁
- ## 反向定位分析
"""


def create_moat_analyst(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## 证据包\n{state.get('evidence_pack', 'N/A')[:3000]}\n\n"
                        f"## JTBD\n{state.get('jtbd_report', 'N/A')}\n\n"
                        f"## Value Prop\n{state.get('value_prop_report', 'N/A')}\n\n"
                        f"## GTM\n{state.get('gtm_report', 'N/A')}\n\n"
                        f"## Unit Econ\n{state.get('unit_econ_report', 'N/A')}\n\n"
                        "请输出护城河与竞争分析。"
                    )
                ),
            ]
        )
        return {"moat_report": response.content}

    return node
