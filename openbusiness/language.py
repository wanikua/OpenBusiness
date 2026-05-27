"""Output language helpers shared by CLI, config, and agent prompts."""

from __future__ import annotations

import re
from typing import Optional


DEFAULT_OUTPUT_LANGUAGE = "zh"
SUPPORTED_OUTPUT_LANGUAGES = ("zh", "en")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

_ALIASES = {
    "zh": "zh",
    "cn": "zh",
    "zh-cn": "zh",
    "chinese": "zh",
    "simplified-chinese": "zh",
    "中文": "zh",
    "en": "en",
    "en-us": "en",
    "english": "en",
    "英文": "en",
}


def normalize_output_language(value: Optional[str], default: str = DEFAULT_OUTPUT_LANGUAGE) -> str:
    """Normalize user/config/env language values to a supported language code."""
    raw = (value or default).strip().lower()
    language = _ALIASES.get(raw)
    if language:
        return language
    raise ValueError(
        f"Unsupported output language: {value!r}. "
        f"Use one of: {', '.join(SUPPORTED_OUTPUT_LANGUAGES)}."
    )


def output_language_name(language: Optional[str]) -> str:
    """Return the English display name for a normalized output language."""
    normalized = normalize_output_language(language)
    return {"zh": "Simplified Chinese", "en": "English"}[normalized]


OUTPUT_TEMPLATES = {
    "evidence_collector": {
        "en": """\
- ## Website & Product Facts
- ## Pricing & Business Model Signals
- ## Customer Proof And Case Studies
- ## Hiring / Organization Signals
- ## Ecosystem And Integration Signals
- ## News & Strategy Updates
- ## Founder / Product Philosophy
- ## Funding And Investors
- ## Financial Facts (Public Companies)
- ## Competitive Landscape
- ## Source Reliability Notes
- ## Missing Data""",
        "zh": """\
- ## 官网与产品事实
- ## 定价与商业模式信号
- ## 客户证据与案例
- ## 招聘与组织信号
- ## 生态与集成信号
- ## 新闻与战略动态
- ## 创始人和产品理念
- ## 融资与投资人
- ## 财务事实（上市公司）
- ## 竞争环境
- ## 来源可靠性说明
- ## 数据缺口""",
    },
    "jtbd_analyst": {
        "en": """\
- ## Buyer / Decision Maker
- ## End User Segments
- ## Job To Be Done
- ## Switching Trigger And Urgency
- ## Alternative Behavior
- ## Willingness-To-Pay Signals
- ## Open Validation Questions""",
        "zh": """\
- ## 付费者 / 决策者
- ## 使用者细分
- ## 待完成任务
- ## 切换触发点与紧迫性
- ## 替代行为
- ## 付费意愿信号
- ## 待验证问题""",
    },
    "value_prop_analyst": {
        "en": """\
- ## Core Value
- ## Before / After Delta
- ## 10x Better Test
- ## Tradeoffs And Adoption Friction
- ## Value Type
- ## Durability Of Value
- ## Validation Gaps""",
        "zh": """\
- ## 核心价值
- ## 使用前后变化
- ## 十倍优势测试
- ## 取舍与采用阻力
- ## 价值类型
- ## 价值可持续性
- ## 验证缺口""",
    },
    "gtm_analyst": {
        "en": """\
- ## Primary Channels
- ## Secondary Channels
- ## Channel Evidence Matrix
- ## Sales Motion And ICP
- ## Growth Loop Hypothesis
- ## Channel Economics
- ## Channel Risks""",
        "zh": """\
- ## 主渠道
- ## 次渠道
- ## 渠道证据矩阵
- ## 销售动作与理想客户画像
- ## 增长飞轮假设
- ## 渠道经济性
- ## 渠道风险""",
    },
    "unit_econ_analyst": {
        "en": """\
- ## Monetization Model
- ## Key Metrics
- ## Scenario Assumptions
- ## Unit Economics Calculation
- ## Sensitivity Analysis
- ## Health Assessment And Risks
- ## Data That Would Change The Conclusion""",
        "zh": """\
- ## 变现模式
- ## 关键指标
- ## 情景假设
- ## 单体经济计算
- ## 敏感性分析
- ## 健康度评价与风险
- ## 可能改变结论的数据""",
    },
    "moat_analyst": {
        "en": """\
- ## Five Moat Ratings
- ## Competitor Map
- ## Strongest Moat And Weakest Link
- ## Key Competitive Threats
- ## Counter-Positioning Analysis
- ## Time-Decay Risk
- ## Tests To Validate The Moat""",
        "zh": """\
- ## 五类壁垒评级
- ## 竞争者地图
- ## 最强壁垒与最弱环节
- ## 关键竞争威胁
- ## 反向定位分析
- ## 时间衰减风险
- ## 壁垒验证测试""",
    },
    "synthesizer": {
        "en": """\
## Strategic Thesis
## At-a-Glance Verdict

| Field | Verdict | Evidence |
| :--- | :--- | :--- |
| Customer | ... | ... |
| Buyer | ... | ... |
| User | ... | ... |
| Market Type | ToB / ToC / B2B / B2C / B2B2C / Marketplace / Developer Platform / Mixed | ... |
| Business Model | Subscription / Usage-based / Transaction fee / Ads / Services / Hardware / Mixed | ... |
| Funding Stage | Pre-Seed / Seed / Series A / Series B / Series C+ / Growth / Public / Bootstrapped / No announced financing plan / Not found | ... |
| Latest Valuation | ... | ... |
| Moat Verdict | Strong / Moderate / Weak / None | ... |
| Outlook | Strong / Positive / Mixed / Weak / Unknown | ... |
| Biggest Risk | ... | ... |

## Business Model Canvas

| Key Partners | Key Activities | Value Propositions | Customer Relationships | Customer Segments |
| :--- | :--- | :--- | :--- | :--- |
| ... [VERIFIED:...] | ... [INFERRED] | **Core Value:** ... | ... | ... |
| | **Key Resources:** ... | | **Channels:** ... | |

| Cost Structure | Revenue Streams |
| :--- | :--- |
| ... | ... |

## Profit Engine
## Customer And Market Type
## Funding And Investor Signals
## Causal Chain
## Unit Economics Snapshot
## Moat Snapshot
## Non-Obvious Insights
## Verified Facts
## Inferred Assumptions
## Missing Data""",
        "zh": """\
## 战略判断
## 直觉结论卡

| 字段 | 结论 | 证据 |
| :--- | :--- | :--- |
| 客户是谁 | ... | ... |
| 谁付钱 | ... | ... |
| 谁使用 | ... | ... |
| 市场类型 | ToB / ToC / B2B / B2C / B2B2C / Marketplace / Developer Platform / Mixed | ... |
| 商业模式 | 订阅 / 用量计费 / 抽佣 / 广告 / 服务 / 硬件 / 混合 | ... |
| 融资阶段 | Pre-Seed / Seed / A轮 / B轮 / C轮及以后 / Growth / 已上市 / 自举未融资 / 未有融资计划 / 找不到 | ... |
| 最新估值 | ... | ... |
| 护城河判断 | Strong / Moderate / Weak / None | ... |
| 前景判断 | 强 / 偏强 / 中性或分化 / 偏弱 / 未知 | ... |
| 最大风险 | ... | ... |

## 商业模式画布

| 核心伙伴 | 关键业务 | 价值主张 | 客户关系 | 客户细分 |
| :--- | :--- | :--- | :--- | :--- |
| ... [VERIFIED:...] | ... [INFERRED] | **核心价值：**... | ... | ... |
| | **核心资源：**... | | **渠道通路：**... | |

| 成本结构 | 收入来源 |
| :--- | :--- |
| ... | ... |

## 利润引擎
## 客户与市场类型
## 融资与投资人信号
## 因果链条
## 单体经济快照
## 护城河快照
## 非显而易见洞察
## 已验证事实
## 推断假设
## 数据缺口""",
    },
    "stress_tester": {
        "en": """\
## High-Priority Assumptions
- Assumption: ...
  - Falsification condition: ...
  - Failure chain: ...
  - Leading indicator: ...
  - Priority: High

## Medium-Priority Assumptions
## Scenario Reversal Table
## Early Warning Indicators
## Critical Data Gaps
## One-Line Verdict""",
        "zh": """\
## 高优先级假设
- 假设：...
  - 证伪条件：...
  - 失效连锁：...
  - 先行指标：...
  - 优先级：High

## 中优先级假设
## 情景反转表
## 早期预警指标
## 关键数据缺口
## 一句话结论""",
    },
    "finalizer": {
        "en": """\
# OpenBusiness Business Model Reverse Engineering Report

**Target:** [company] | **Confidence:** [Robust/Plausible/Fragile/Speculative]

## 1. Executive Thesis
## 2. At-a-Glance Verdict

| Field | Verdict | Evidence |
| :--- | :--- | :--- |
| Customer | ... | ... |
| Buyer | ... | ... |
| User | ... | ... |
| Market Type | ToB / ToC / B2B / B2C / B2B2C / Marketplace / Developer Platform / Mixed | ... |
| Business Model | Subscription / Usage-based / Transaction fee / Ads / Services / Hardware / Mixed | ... |
| Funding Stage | Pre-Seed / Seed / Series A / Series B / Series C+ / Growth / Public / Bootstrapped / No announced financing plan / Not found | ... |
| Latest Valuation | ... | ... |
| Moat Verdict | Strong / Moderate / Weak / None | ... |
| Outlook | Strong / Positive / Mixed / Weak / Unknown | ... |
| Biggest Risk | ... | ... |
## 3. Business Model Canvas
## 4. Key Fact Layers
### Verified Facts
### Inferred Assumptions
### Missing Data
## 5. Profit Engine
## 6. Funding And Investor Signals
## 7. Strategic Interpretation
## 8. Assumption Stress Test
## 9. Next Steps""",
        "zh": """\
# OpenBusiness 商业模式逆向工程报告

**分析对象：**[公司名] | **可信度：**[Robust/Plausible/Fragile/Speculative]

## 1. 核心判断
## 2. 直觉结论卡

| 字段 | 结论 | 证据 |
| :--- | :--- | :--- |
| 客户是谁 | ... | ... |
| 谁付钱 | ... | ... |
| 谁使用 | ... | ... |
| 市场类型 | ToB / ToC / B2B / B2C / B2B2C / Marketplace / Developer Platform / Mixed | ... |
| 商业模式 | 订阅 / 用量计费 / 抽佣 / 广告 / 服务 / 硬件 / 混合 | ... |
| 融资阶段 | Pre-Seed / Seed / A轮 / B轮 / C轮及以后 / Growth / 已上市 / 自举未融资 / 未有融资计划 / 找不到 | ... |
| 最新估值 | ... | ... |
| 护城河判断 | Strong / Moderate / Weak / None | ... |
| 前景判断 | 强 / 偏强 / 中性或分化 / 偏弱 / 未知 | ... |
| 最大风险 | ... | ... |
## 3. 商业模式画布
## 4. 关键事实分层
### 已验证事实
### 推断假设
### 数据缺口
## 5. 利润引擎
## 6. 融资与投资人信号
## 7. 战略解读
## 8. 假设压力测试
## 9. 下一步建议""",
    },
}

UI_TEXT = {
    "en": {
        "analysis_title": "Business Model Reverse Engineering",
        "target": "Target",
        "no_domain": "no domain",
        "output_language": "Output language",
        "starting_pipeline": "Starting pipeline...",
        "pipeline_no_report": "Pipeline completed but no final report was produced. Check API keys and quota.",
        "report_generated": "Report generated:",
        "preview": "Preview",
        "language_warning_title": "Language purity warning",
    },
    "zh": {
        "analysis_title": "商业模式逆向工程",
        "target": "分析对象",
        "no_domain": "无域名",
        "output_language": "输出语言",
        "starting_pipeline": "启动流水线...",
        "pipeline_no_report": "流水线完成但没有最终报告。请检查 API key 与额度。",
        "report_generated": "报告已生成：",
        "preview": "预览",
        "language_warning_title": "语言纯度警告",
    },
}


def localized_output_template(template_key: str, language: Optional[str]) -> str:
    """Return the required localized output template for one analyst."""
    normalized = normalize_output_language(language)
    return OUTPUT_TEMPLATES[template_key][normalized]


def ui_text(language: Optional[str], key: str) -> str:
    """Return localized CLI text."""
    normalized = normalize_output_language(language)
    return UI_TEXT[normalized][key]


def analytical_depth_instruction(language: Optional[str]) -> str:
    """Prompt fragment that raises the analytical depth bar."""
    normalized = normalize_output_language(language)
    if normalized == "en":
        return (
            "# Analytical Depth Standard\n"
            "Do not stop at classification, summary, or generic best-practice language. "
            "Every major conclusion must include: (1) the mechanism that makes it true, "
            "(2) the evidence quality behind it, (3) the countercase that could make it false, "
            "(4) the business-model implication, and (5) the next validation data required. "
            "Prefer causal chains, quantified ranges, scenario comparisons, and named tradeoffs. "
            "When data is missing, state how sensitive the conclusion is to that missing data "
            "instead of filling the gap with a confident guess. Depth is not length: use "
            "2-4 high-signal bullets per section, avoid restating upstream text, and prioritize "
            "the few drivers that can change the conclusion."
        )
    return (
        "# 分析深度标准\n"
        "不要停留在分类、摘要或通用套话。每个重要结论都必须说明："
        "（1）结论成立的机制，（2）背后的证据强度，（3）可能推翻它的反例，"
        "（4）对商业模式的影响，（5）下一步需要验证的数据。优先输出因果链条、"
        "量化区间、情景对比和明确取舍。数据缺失时，要说明结论对该数据的敏感度，"
        "不要用自信猜测填补缺口。深度不是篇幅：每节使用 2-4 条高信号要点，"
        "避免复述上游原文，优先写出少数真正会改变结论的驱动因素。"
    )


def output_language_instruction(language: Optional[str]) -> str:
    """Prompt fragment that makes the requested report language explicit."""
    normalized = normalize_output_language(language)
    name = output_language_name(normalized)
    output_discipline = (
        " Output only the requested Markdown content. Do not include preambles, "
        "meta commentary, tool-use narration, or sentences such as 'Okay', '好的', "
        "'I will now', or 'Here is'."
    )
    if normalized == "en":
        return (
            "# Output Language\n"
            "Write all generated analysis and Markdown report content in pure English. "
            "This instruction has higher priority than any earlier example output format. "
            "Translate any example headings, table labels, recommendations, and summaries "
            "into English while preserving the same structure. Keep company names, URLs, "
            "tool names, numeric values, and evidence tags such as [VERIFIED:url], "
            "[INFERRED], and [MISSING] unchanged. Do not mix Chinese into the output "
            "unless it appears inside quoted source evidence. Translate any upstream Chinese "
            "headings or prose into English before final output."
            f"{output_discipline}"
        )
    return (
        "# Output Language\n"
        f"Write all generated analysis and Markdown report content in pure {name}. "
        "All natural-language prose, headings, table labels, recommendations, and summaries "
        "must be Simplified Chinese. Translate upstream English headings or prose into "
        "Simplified Chinese before final output. Keep company names, URLs, ticker symbols, "
        "standard metric abbreviations such as ARPU, LTV, CAC, LTV/CAC, PLG, API/tool/model "
        "names, numeric values, and evidence tags such as [VERIFIED:url], [INFERRED], and "
        "[MISSING] unchanged."
        f"{output_discipline}"
    )


def with_output_language(
    system_prompt: str,
    language: Optional[str],
    template_key: Optional[str] = None,
) -> str:
    """Append the output-language contract to an agent system prompt."""
    prompt = (
        f"{system_prompt.rstrip()}\n\n"
        f"{analytical_depth_instruction(language)}\n\n"
        f"{output_language_instruction(language)}"
    )
    if template_key:
        prompt += (
            "\n\n# Required Localized Output Template\n"
            "Use the localized headings below. They override any earlier output examples. "
            "Do not output headings from another language.\n\n"
            f"{localized_output_template(template_key, language)}"
        )
    return prompt


def report_language_warnings(text: str, language: Optional[str], max_examples: int = 5) -> list[str]:
    """Return human-readable warnings when a generated report is not language-pure."""
    normalized = normalize_output_language(language)
    warnings: list[str] = []

    if normalized == "en":
        examples = [line.strip() for line in text.splitlines() if CJK_RE.search(line)]
        if examples:
            warnings.append(
                "English report contains Chinese characters in lines: "
                + " | ".join(examples[:max_examples])
            )
        return warnings

    heading_pattern = re.compile(
        r"^#{1,6}\s+(Business Model|Key Fact|Verified Facts|Inferred Assumptions|"
        r"Missing Data|Assumption Stress Test|Next Steps|Unit Economics|Moat Snapshot)",
        re.MULTILINE,
    )
    if not CJK_RE.search(text):
        warnings.append("Chinese report contains no Chinese characters.")
    english_headings = heading_pattern.findall(text)
    if english_headings:
        warnings.append(
            "Chinese report contains English section headings: "
            + ", ".join(english_headings[:max_examples])
        )
    english_like_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or CJK_RE.search(stripped):
            continue
        if stripped.startswith(("---", "| :---", "| ---")):
            continue
        words = re.findall(r"[A-Za-z]{3,}", stripped)
        if len(words) >= 6:
            english_like_lines.append(stripped)
    if english_like_lines:
        warnings.append(
            "Chinese report contains English-like prose lines: "
            + " | ".join(english_like_lines[:max_examples])
        )
    return warnings
