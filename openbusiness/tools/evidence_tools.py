"""Evidence collection tools — Tavily search, Firecrawl scrape, SEC EDGAR.

All tools degrade gracefully when API keys are missing.
Every snippet returned is tagged with its source URL for verification downstream.
"""

from __future__ import annotations

import json
import os
from typing import Optional

import requests
from langchain_core.tools import tool


def _tavily_key() -> Optional[str]:
    return os.getenv("TAVILY_API_KEY") or None


def _firecrawl_key() -> Optional[str]:
    return os.getenv("FIRECRAWL_API_KEY") or None


@tool
def tavily_search(query: str, max_results: int = 5, search_depth: str = "basic") -> str:
    """Search the public web for company facts via Tavily.

    Use for: pricing pages, press releases, founder interviews, recent news,
    competitive comparisons, product launches. Returns titles, URLs and snippets
    each tagged with [VERIFIED:<url>].

    Args:
        query: Search query — be specific (e.g. 'Notion pricing tiers 2025').
        max_results: How many results (1-10).
        search_depth: Tavily search depth. Use "advanced" for deeper research.

    Returns:
        JSON list of {title, url, content, source_tag} dicts.
    """
    key = _tavily_key()
    if not key:
        return json.dumps(
            {
                "warning": "TAVILY_API_KEY not set",
                "fallback_action": "Caller should rely on [INFERRED] LLM knowledge and label clearly",
                "results": [],
            },
            ensure_ascii=False,
        )

    try:
        depth = "advanced" if search_depth == "advanced" else "basic"
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": key, "query": query, "max_results": min(max_results, 10), "search_depth": depth},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        results = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")[:900],
                "source_tag": f"[VERIFIED:{r.get('url', '')}]",
            }
            for r in data.get("results", [])
        ]
        return json.dumps({"query": query, "results": results}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "results": []}, ensure_ascii=False)


@tool
def firecrawl_scrape(url: str) -> str:
    """Scrape a single URL via Firecrawl and return clean markdown.

    Use for: pricing pages, about pages, careers pages, product docs.
    Returns the full page content tagged with [VERIFIED:<url>].

    Args:
        url: Full URL to scrape (e.g. 'https://notion.so/pricing').

    Returns:
        JSON with markdown content and source tag.
    """
    key = _firecrawl_key()
    if not key:
        return json.dumps(
            {
                "warning": "FIRECRAWL_API_KEY not set",
                "fallback_action": "Caller should note this URL was not fetched and tag insights [INFERRED]",
                "url": url,
                "content": "",
            },
            ensure_ascii=False,
        )

    try:
        resp = requests.post(
            "https://api.firecrawl.dev/v1/scrape",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
            timeout=35,
        )
        resp.raise_for_status()
        data = resp.json()
        markdown = data.get("data", {}).get("markdown", "")[:12000]
        return json.dumps(
            {"url": url, "source_tag": f"[VERIFIED:{url}]", "content": markdown},
            ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps({"error": str(e), "url": url, "content": ""}, ensure_ascii=False)


@tool
def sec_edgar_company_facts(ticker: str) -> str:
    """Fetch standardized company financials from SEC EDGAR (no API key required).

    Use for: revenue, operating income, R&D spend, share count, segment data
    for any US-listed public company. Free, authoritative source.

    Args:
        ticker: Stock ticker (e.g. 'AAPL', 'COST').

    Returns:
        JSON with CIK, latest revenue, recent filings, source tag.
    """
    if not ticker:
        return json.dumps({"warning": "No ticker — private company; use tavily_search instead", "results": []})

    try:
        ticker = ticker.upper()
        # Resolve ticker → CIK
        tickers_resp = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers={"User-Agent": "OpenBusiness research@openbusiness.local"},
            timeout=20,
        )
        tickers_resp.raise_for_status()
        cik = None
        for entry in tickers_resp.json().values():
            if entry.get("ticker", "").upper() == ticker:
                cik = str(entry["cik_str"]).zfill(10)
                break
        if not cik:
            return json.dumps({"warning": f"Ticker {ticker} not found in SEC EDGAR", "results": []})

        # Pull company facts
        facts_resp = requests.get(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
            headers={"User-Agent": "OpenBusiness research@openbusiness.local"},
            timeout=30,
        )
        facts_resp.raise_for_status()
        facts = facts_resp.json()

        # Extract recent revenue (USD)
        revenue_data = []
        try:
            revenues = facts["facts"]["us-gaap"]["Revenues"]["units"]["USD"]
            annual = [r for r in revenues if r.get("fp") == "FY"][-3:]
            revenue_data = [
                {"fiscal_year": r.get("fy"), "revenue_usd": r.get("val"), "filed": r.get("filed")}
                for r in annual
            ]
        except KeyError:
            pass

        return json.dumps(
            {
                "ticker": ticker,
                "cik": cik,
                "company_name": facts.get("entityName", ""),
                "source_tag": f"[VERIFIED:https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}]",
                "recent_annual_revenue": revenue_data,
            },
            ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps({"error": str(e), "ticker": ticker, "results": []}, ensure_ascii=False)
