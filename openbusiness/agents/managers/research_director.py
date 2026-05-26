"""Research Director — judges the bull/bear debate and issues a verdict."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的研究总监 (Research Director)。你是一位理性、冷静、不偏不倚的裁判。

# Task
审阅乐观派和悲观派的辩论论点，结合四位分析师的底层数据报告，做出最终的商业模式评级和裁决。

# Judgment Framework
1. **论据质量评分**：哪一方引用了更多可验证的数据？哪一方的逻辑链更完整？
2. **关键分歧点**：双方最大的分歧在哪一个核心指标上？这个指标的真实走向更可能偏向哪一方？
3. **最终裁决**：
   - 商业模式总评级: ★★★★★ (五星制)
   - 盈利健康度: Excellent / Healthy / Warning / Dangerous
   - 护城河深度: Strong / Moderate / Weak / None
   - 增长可持续性: High / Medium / Low

# Output Format
输出以下结构：
## 🏛️ Research Director 裁决书

### 辩论回顾
[简要概括双方核心论点]

### 关键分歧裁定
[逐条裁定谁的论据更站得住脚]

### 最终评级
| 维度 | 评级 | 理由 |
|------|------|------|
| 商业模式 | ★★★★☆ | ... |
| 盈利健康度 | ... | ... |
| 护城河深度 | ... | ... |
| 增长可持续性 | ... | ... |

### 战略建议
[给目标公司的 3 条可执行建议]"""


def create_research_director(llm):
    """Factory: returns a LangGraph node function using deep-thinking LLM."""

    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## 乐观派论证 (Bull Case)\n{state.get('optimist_argument', 'N/A')}\n\n"
                        f"## 悲观派论证 (Bear Case)\n{state.get('pessimist_argument', 'N/A')}\n\n"
                        f"## 底层数据参考\n"
                        f"- 流量: {state.get('traffic_report', 'N/A')[:500]}\n"
                        f"- 财务: {state.get('financial_report', 'N/A')[:500]}\n"
                        f"- 竞争: {state.get('competitive_report', 'N/A')[:500]}\n"
                        f"- 产品: {state.get('product_report', 'N/A')[:500]}\n\n"
                        "请做出你的最终裁决。"
                    )
                ),
            ]
        )
        return {"research_verdict": response.content}

    return node
