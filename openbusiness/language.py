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
- ## News & Strategy Updates
- ## Founder / Product Philosophy
- ## Financial Facts (Public Companies)
- ## Competitive Landscape
- ## Missing Data""",
        "zh": """\
- ## 官网与产品事实
- ## 定价与商业模式信号
- ## 新闻与战略动态
- ## 创始人和产品理念
- ## 财务事实（上市公司）
- ## 竞争环境
- ## 数据缺口""",
    },
    "jtbd_analyst": {
        "en": """\
- ## Buyer / Decision Maker
- ## End User
- ## Job To Be Done
- ## Alternative Behavior""",
        "zh": """\
- ## 付费者 / 决策者
- ## 使用者
- ## 待完成任务
- ## 替代行为""",
    },
    "value_prop_analyst": {
        "en": """\
- ## Core Value
- ## 10x Better Test
- ## Value Type""",
        "zh": """\
- ## 核心价值
- ## 十倍优势测试
- ## 价值类型""",
    },
    "gtm_analyst": {
        "en": """\
- ## Primary Channels
- ## Secondary Channels
- ## Evidence Signals
- ## Channel Risks""",
        "zh": """\
- ## 主渠道
- ## 次渠道
- ## 证据信号
- ## 渠道风险""",
    },
    "unit_econ_analyst": {
        "en": """\
- ## Monetization Model
- ## Key Metrics
- ## Unit Economics Calculation
- ## Health Assessment And Risks""",
        "zh": """\
- ## 变现模式
- ## 关键指标
- ## 单体经济计算
- ## 健康度评价与风险""",
    },
    "moat_analyst": {
        "en": """\
- ## Five Moat Ratings
- ## Key Competitive Threats
- ## Counter-Positioning Analysis""",
        "zh": """\
- ## 五类壁垒评级
- ## 关键竞争威胁
- ## 反向定位分析""",
    },
    "synthesizer": {
        "en": """\
## Business Model Canvas

| Key Partners | Key Activities | Value Propositions | Customer Relationships | Customer Segments |
| :--- | :--- | :--- | :--- | :--- |
| ... [VERIFIED:...] | ... [INFERRED] | **Core Value:** ... | ... | ... |
| | **Key Resources:** ... | | **Channels:** ... | |

| Cost Structure | Revenue Streams |
| :--- | :--- |
| ... | ... |

## Unit Economics Snapshot
## Moat Snapshot
## Verified Facts
## Inferred Assumptions
## Missing Data""",
        "zh": """\
## 商业模式画布

| 核心伙伴 | 关键业务 | 价值主张 | 客户关系 | 客户细分 |
| :--- | :--- | :--- | :--- | :--- |
| ... [VERIFIED:...] | ... [INFERRED] | **核心价值：**... | ... | ... |
| | **核心资源：**... | | **渠道通路：**... | |

| 成本结构 | 收入来源 |
| :--- | :--- |
| ... | ... |

## 单体经济快照
## 护城河快照
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
  - Priority: High

## Medium-Priority Assumptions
## Critical Data Gaps
## One-Line Verdict""",
        "zh": """\
## 高优先级假设
- 假设：...
  - 证伪条件：...
  - 失效连锁：...
  - 优先级：High

## 中优先级假设
## 关键数据缺口
## 一句话结论""",
    },
    "finalizer": {
        "en": """\
# OpenBusiness Business Model Reverse Engineering Report

**Target:** [company] | **Confidence:** [Robust/Plausible/Fragile/Speculative]

## 1. Business Model Canvas
## 2. Key Fact Layers
### Verified Facts
### Inferred Assumptions
### Missing Data
## 3. Assumption Stress Test
## 4. Next Steps""",
        "zh": """\
# OpenBusiness 商业模式逆向工程报告

**分析对象：**[公司名] | **可信度：**[Robust/Plausible/Fragile/Speculative]

## 1. 商业模式画布
## 2. 关键事实分层
### 已验证事实
### 推断假设
### 数据缺口
## 3. 假设压力测试
## 4. 下一步建议""",
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


def output_language_instruction(language: Optional[str]) -> str:
    """Prompt fragment that makes the requested report language explicit."""
    normalized = normalize_output_language(language)
    name = output_language_name(normalized)
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
    )


def with_output_language(
    system_prompt: str,
    language: Optional[str],
    template_key: Optional[str] = None,
) -> str:
    """Append the output-language contract to an agent system prompt."""
    prompt = f"{system_prompt.rstrip()}\n\n{output_language_instruction(language)}"
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
