"""Evidence collection tools — Tavily search, Firecrawl scrape, SEC EDGAR.

All tools degrade gracefully when API keys are missing.
Every snippet returned is tagged with its source URL for verification downstream.
"""

from __future__ import annotations

import os
from typing import Optional

import requests
from langchain_core.tools import tool

from openbusiness.evidence import error_result, missing_result, source_tag, verified_result


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
        return missing_result(
            "tavily_search",
            "TAVILY_API_KEY not set",
            "Caller should rely on [INFERRED] LLM knowledge and label clearly.",
            results=[],
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
                "source_tag": source_tag(r.get("url", "")),
            }
            for r in data.get("results", [])
        ]
        return verified_result("tavily_search", query=query, results=results)
    except Exception as e:
        return error_result("tavily_search", str(e), query=query, results=[])


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
        return missing_result(
            "firecrawl_scrape",
            "FIRECRAWL_API_KEY not set",
            "Caller should note this URL was not fetched and tag insights [INFERRED].",
            url=url,
            content="",
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
        return verified_result("firecrawl_scrape", url=url, source_tag=source_tag(url), content=markdown)
    except Exception as e:
        return error_result("firecrawl_scrape", str(e), url=url, content="")


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
        return missing_result(
            "sec_edgar_company_facts",
            "No ticker - private company; use tavily_search instead.",
            "Use tavily_search for private-company evidence.",
            results=[],
        )

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
            return missing_result(
                "sec_edgar_company_facts",
                f"Ticker {ticker} not found in SEC EDGAR.",
                "Use tavily_search for non-US-listed or private-company evidence.",
                ticker=ticker,
                results=[],
            )

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

        source_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
        return verified_result(
            "sec_edgar_company_facts",
            ticker=ticker,
            cik=cik,
            company_name=facts.get("entityName", ""),
            source_tag=source_tag(source_url),
            recent_annual_revenue=revenue_data,
        )
    except Exception as e:
        return error_result("sec_edgar_company_facts", str(e), ticker=ticker, results=[])
