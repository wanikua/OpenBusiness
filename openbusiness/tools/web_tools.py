"""Web scraping and data retrieval tools.

Provide real-world data gathering capabilities for analysts.
"""

from __future__ import annotations

import json

from langchain_core.tools import tool


@tool
def fetch_company_overview(company_name: str) -> str:
    """Fetch public overview data for a company.

    Searches for company information including industry, founding year,
    employee count, headquarters, and public description.

    Args:
        company_name: The company name to research.

    Returns:
        JSON with company overview data.
    """
    # In production, this would call real APIs (Crunchbase, SEC Edgar, etc.)
    # For now, return a structured placeholder that the LLM will populate
    # based on its knowledge, clearly marked as needing real data enrichment
    return json.dumps(
        {
            "company": company_name,
            "data_source": "llm_knowledge",
            "note": "Production version should integrate Crunchbase/SEC/Yahoo Finance APIs",
            "fields_to_populate": [
                "industry",
                "founded_year",
                "headquarters",
                "employee_count",
                "funding_stage",
                "last_valuation",
                "key_products",
                "target_market",
            ],
        },
        ensure_ascii=False,
    )


@tool
def fetch_pricing_page(domain: str) -> str:
    """Analyze a SaaS company's pricing page structure.

    Args:
        domain: Company website domain (e.g. 'notion.so').

    Returns:
        JSON with pricing tier analysis prompts.
    """
    return json.dumps(
        {
            "domain": domain,
            "data_source": "llm_knowledge",
            "note": "Production version should scrape actual pricing pages",
            "analysis_framework": {
                "tiers_to_identify": [
                    "Free tier (功能限制 & 用户上限)",
                    "Pro/Plus tier (个人付费)",
                    "Team/Business tier (团队协作)",
                    "Enterprise tier (大客户定制)",
                ],
                "key_metrics": [
                    "price_per_seat_monthly",
                    "free_to_paid_conversion_triggers",
                    "enterprise_custom_pricing_signals",
                ],
            },
        },
        ensure_ascii=False,
    )
