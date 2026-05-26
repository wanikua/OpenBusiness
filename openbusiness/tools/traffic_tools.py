"""Traffic & channel analysis tools.

Provide deterministic data about a company's online presence,
traffic sources, and customer acquisition channels.
"""

from __future__ import annotations

import json

from langchain_core.tools import tool


@tool
def analyze_traffic_channels(
    direct_pct: float,
    organic_search_pct: float,
    paid_ads_pct: float,
    social_referral_pct: float,
    email_pct: float = 0.0,
) -> str:
    """Analyze traffic channel distribution and diagnose acquisition health.

    Args:
        direct_pct: Percentage of traffic from direct visits.
        organic_search_pct: Percentage from organic search (SEO).
        paid_ads_pct: Percentage from paid advertising.
        social_referral_pct: Percentage from social media & referrals.
        email_pct: Percentage from email marketing (optional).

    Returns:
        JSON with channel breakdown, primary driver, and acquisition risk assessment.
    """
    channels = {
        "Direct": direct_pct,
        "Organic Search (SEO)": organic_search_pct,
        "Paid Ads": paid_ads_pct,
        "Social/Referral": social_referral_pct,
        "Email": email_pct,
    }

    primary = max(channels, key=channels.get)
    organic_total = direct_pct + organic_search_pct

    if paid_ads_pct > 50:
        risk = "High — 过度依赖付费投放，CAC 随竞价水涨船高，利润极脆弱"
        growth_model = "Paid Acquisition (烧钱买量)"
    elif organic_total > 60:
        risk = "Low — 自然流量为主，获客成本可控，具备 PLG 特征"
        growth_model = "Product-Led Growth (产品驱动增长)"
    elif social_referral_pct > 40:
        risk = "Medium — 依赖社交传播，流量波动大，需防平台算法变化"
        growth_model = "Viral/Community-Led (社区驱动增长)"
    else:
        risk = "Balanced — 流量来源分散，抗风险能力较好"
        growth_model = "Hybrid (混合获客)"

    return json.dumps(
        {
            "channels": {k: f"{v}%" for k, v in channels.items()},
            "primary_channel": primary,
            "organic_ratio": f"{round(organic_total, 1)}%",
            "acquisition_risk": risk,
            "growth_model": growth_model,
        },
        ensure_ascii=False,
    )


@tool
def analyze_seo_moat(
    monthly_organic_visits: int,
    top_keywords: list[str],
    domain_authority: int,
    branded_search_pct: float,
) -> str:
    """Evaluate a company's SEO moat strength.

    Args:
        monthly_organic_visits: Estimated monthly organic search visits.
        top_keywords: List of top-ranking keywords.
        domain_authority: Domain authority score (0-100).
        branded_search_pct: Percentage of organic traffic from branded queries.

    Returns:
        JSON with SEO moat rating and analysis.
    """
    if domain_authority >= 70 and branded_search_pct >= 40:
        moat = "Strong — 品牌心智已建立，搜索引擎地位稳固"
    elif domain_authority >= 50:
        moat = "Moderate — 有一定 SEO 积累，但可被后来者追赶"
    else:
        moat = "Weak — SEO 壁垒低，流量容易被抢"

    return json.dumps(
        {
            "monthly_organic_visits": monthly_organic_visits,
            "top_keywords": top_keywords[:10],
            "domain_authority": domain_authority,
            "branded_search_share": f"{branded_search_pct}%",
            "seo_moat_rating": moat,
        },
        ensure_ascii=False,
    )
