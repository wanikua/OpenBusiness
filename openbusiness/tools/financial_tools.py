"""Deterministic unit-economics calculator.

Pure math, no LLM. Output includes a `[VERIFIED:calculation]` tag so
downstream agents know these numbers came from real arithmetic, not guesses.
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
    """Compute LTV, LTV/CAC, break-even users for a business model.

    Args:
        arpu: Average Revenue Per User (per period).
        churn_rate: Period churn (e.g. 0.05 = 5%).
        gross_margin: Margin ratio (e.g. 0.80 = 80%).
        cac: Customer Acquisition Cost.
        fixed_cost: Total fixed cost per period.

    Returns:
        JSON with LTV, LTV/CAC ratio, break-even users, and health verdict.
        All values tagged [VERIFIED:calculation] since they're deterministic.
    """
    user_lifetime = 1 / churn_rate if churn_rate > 0 else 100
    ltv = arpu * gross_margin * user_lifetime
    ltv_cac = ltv / cac if cac > 0 else float("inf")
    contribution = arpu * gross_margin
    break_even = int(fixed_cost / contribution) if contribution > 0 else 0

    if ltv_cac >= 5:
        health = "Excellent — 高效印钞机"
    elif ltv_cac >= 3:
        health = "Healthy — 健康飞轮"
    elif ltv_cac >= 1.5:
        health = "Warning — 获客效率偏低"
    else:
        health = "Dangerous — 流血扩张"

    return json.dumps(
        {
            "source": "[VERIFIED:calculation]",
            "inputs": {"arpu": arpu, "churn_rate": churn_rate, "gross_margin": gross_margin, "cac": cac, "fixed_cost": fixed_cost},
            "user_lifetime_periods": round(user_lifetime, 2),
            "ltv": round(ltv, 2),
            "ltv_cac_ratio": round(ltv_cac, 2),
            "single_user_contribution": round(contribution, 2),
            "break_even_users_needed": break_even,
            "health_status": health,
        },
        ensure_ascii=False,
    )
