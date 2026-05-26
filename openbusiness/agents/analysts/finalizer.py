"""Finalizer — produces the user-facing terminal report.

Combines the Canvas + Stress Test into a single Markdown document
with clean separation of facts vs assumptions vs gaps.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from openbusiness.agents.utils.agent_state import AgentState

SYSTEM_PROMPT = """\
# Role
你是 OpenBusiness 的报告整理员 (Finalizer)。

# Task
把上游的 Canvas 报告和 Stress Test 报告拼成最终的用户报告。**不要重写内容，只做整合与排版。**

# Output Structure (严格按此格式)

# 📊 OpenBusiness 商业模式逆向工程报告

**Target:** [公司名] | **Confidence:** [Robust/Plausible/Fragile/Speculative]

---

## 1. 商业模式画布
[Canvas 报告原文]

---

## 2. 关键事实层级
### 🟢 Verified Facts (有源)
[从 Canvas 提取所有 [VERIFIED:url] 条目]

### 🟡 Inferred Assumptions (需验证)
[从 Canvas 提取所有 [INFERRED] 条目]

### 🔴 Missing Data (影响信心)
[从 Canvas 提取所有 [MISSING] 条目]

---

## 3. 假设压力测试
[Stress Test 报告原文]

---

## 4. 下一步建议
基于上面的分析，给用户 3 条可执行建议：
- 如果要继续深挖这家公司，应该补充哪些数据？
- 如果要复制其商业模式，最值得抄的是什么？
- 如果要切入相同市场，致命软肋在哪？
"""


def create_finalizer(llm):
    def node(state: AgentState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"目标公司: {state['company_name']}\n\n"
                        f"## Canvas\n{state.get('canvas_report', 'N/A')}\n\n"
                        f"## Stress Test\n{state.get('stress_test_report', 'N/A')}\n\n"
                        "请整合输出最终报告。"
                    )
                ),
            ]
        )
        return {"final_report": response.content}

    return node
