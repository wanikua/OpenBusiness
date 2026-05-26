"""Deterministic financial analysis tools.

These are @tool-decorated functions that analysts call via LangGraph ToolNode.
They provide hard numbers — no LLM hallucination allowed here.
"""

from __future__ import annotations

import json

from langchain_core.tools import tool


@tool
def calculate_unit_economics(
    arpu: float,
    churn_rate: float,
    gross_margin: float,
    cac: float,
    fixed_cost: float = 0.0,
) -> str:
    """Calculate unit economics health for a business model.

    Args:
        arpu: Average Revenue Per User (monthly or annual).
        churn_rate: User churn rate per period (e.g. 0.05 = 5%).
        gross_margin: Gross margin ratio (e.g. 0.80 = 80%).
        cac: Customer Acquisition Cost.
        fixed_cost: Total fixed operating cost per period (optional).

    Returns:
        JSON string with LTV, CAC ratio, break-even users, and health verdict.
    """
    user_lifetime = 1 / churn_rate if churn_rate > 0 else 100
    ltv = arpu * gross_margin * user_lifetime
    ltv_cac_ratio = ltv / cac if cac > 0 else float("inf")

    contribution = arpu * gross_margin
    break_even_users = int(fixed_cost / contribution) if contribution > 0 else 0

    if ltv_cac_ratio >= 5:
        health = "Excellent — 高效印钞机，获客投入产出比极高"
    elif ltv_cac_ratio >= 3:
        health = "Healthy — 盈利飞轮运转良好，有优化空间"
    elif ltv_cac_ratio >= 1.5:
        health = "Warning — 获客效率偏低，需关注留存或降低 CAC"
    else:
        health = "Dangerous — 流血扩张模式，每获一个客户都在亏钱"

    return json.dumps(
        {
            "arpu": arpu,
            "churn_rate": churn_rate,
            "gross_margin": gross_margin,
            "cac": cac,
            "user_lifetime_periods": round(user_lifetime, 2),
            "ltv": round(ltv, 2),
            "ltv_cac_ratio": round(ltv_cac_ratio, 2),
            "health_status": health,
            "single_user_contribution": round(contribution, 2),
            "break_even_users_needed": break_even_users,
        },
        ensure_ascii=False,
    )


@tool
def analyze_revenue_structure(
    revenue_segments: dict[str, float],
    total_revenue: float,
) -> str:
    """Analyze a company's revenue structure by segment.

    Args:
        revenue_segments: Dict mapping segment name to revenue amount.
        total_revenue: Total revenue for normalization.

    Returns:
        JSON with percentage breakdown, concentration risk, and monetization type tags.
    """
    breakdown = {}
    max_pct = 0.0
    max_segment = ""

    for seg, amount in revenue_segments.items():
        pct = round(amount / total_revenue * 100, 1) if total_revenue > 0 else 0
        breakdown[seg] = f"{pct}%"
        if pct > max_pct:
            max_pct = pct
            max_segment = seg

    if max_pct > 70:
        concentration = "High — 单一业务依赖度过高，抗风险能力弱"
    elif max_pct > 50:
        concentration = "Moderate — 核心业务突出，但有一定多元化"
    else:
        concentration = "Diversified — 收入来源分散，抗周期能力强"

    return json.dumps(
        {
            "breakdown": breakdown,
            "dominant_segment": max_segment,
            "dominant_share": f"{max_pct}%",
            "concentration_risk": concentration,
        },
        ensure_ascii=False,
    )


@tool
def calculate_profitability(
    unit_price: float,
    fulfillment_cost: float,
    purchase_frequency: float,
    cac: float,
) -> str:
    """Apply the core profitability formula: Profit = (Price - Cost) * Freq - CAC.

    Args:
        unit_price: Average order value / unit price.
        fulfillment_cost: Per-unit fulfillment + COGS.
        purchase_frequency: Average purchases per user per period.
        cac: Customer acquisition cost.

    Returns:
        JSON with per-user profit, margin, and viability verdict.
    """
    per_user_revenue = unit_price * purchase_frequency
    per_user_cost = fulfillment_cost * purchase_frequency + cac
    per_user_profit = per_user_revenue - per_user_cost
    margin = per_user_profit / per_user_revenue if per_user_revenue > 0 else 0

    if margin > 0.3:
        verdict = "Strong — 单客利润丰厚，模式可规模化"
    elif margin > 0.1:
        verdict = "Viable — 有利润但空间不大，依赖规模效应"
    elif margin > 0:
        verdict = "Thin — 微利，容易被成本波动击穿"
    else:
        verdict = "Loss — 每个用户都在亏损，需重构定价或降本"

    return json.dumps(
        {
            "per_user_revenue": round(per_user_revenue, 2),
            "per_user_total_cost": round(per_user_cost, 2),
            "per_user_profit": round(per_user_profit, 2),
            "profit_margin": f"{round(margin * 100, 1)}%",
            "verdict": verdict,
        },
        ensure_ascii=False,
    )
