# Show HN Post — OpenBusiness

## Title

`Show HN: OpenBusiness – Tag every claim in an AI-generated business model analysis`

(78 chars. Avoid "AI-powered" / "revolutionary"; HN allergic to both.)

## URL field

`https://github.com/wanikua/OpenBusiness`

## Body

I got annoyed at "AI business analysis" tools that confidently invent ARPU, churn, and CAC numbers when a company is private. So I built one that's forced to tag every claim:

- 🟢 `[VERIFIED:url]` — sourced from real evidence (Tavily search, Firecrawl scrape, SEC EDGAR)
- 🟡 `[INFERRED]` — LLM inference from context
- 🔴 `[MISSING]` — couldn't verify, flagged because it affects confidence

The novel mechanic (for me, at least) is the Assumption Stress Tester at the end. It tells you which assumption, if wrong, breaks the entire canvas. Example output from running it on Notion: "If actual monthly churn is 6% instead of the inferred 4%, LTV drops to $160 and LTV/CAC falls to 1.07x — the unit economics flip from 'warning' to 'fatal'."

Pipeline is 9 agents in a linear flow (LangGraph). Inspired by TradingAgents but I deliberately didn't copy the bull/bear debate — business analysis output is a decomposition, not a buy/sell vote.

Two implementation details that took longest to get right:
1. Unit economics is a Python function, not an LLM call. LLMs can't multiply reliably; the analyst's job is to *populate* the inputs (with tags), then the math runs.
2. Two-tier model routing: mini/haiku for the analysts, a deep model for the synthesizer and stress tester. Roughly 10x cheaper than running everything on a frontier model.

Limitations I'll be honest about: it can't verify private-company financials, so private companies get a higher 🟡/🔴 ratio. Without Tavily and Firecrawl keys (both have free tiers), it leans heavily on the LLM's training data and the report is fragile. Reports take 2-4 minutes and cost $0.10–$0.40 in API calls depending on provider.

Sample reports for Notion, Vercel, and OpenAI are in `output/` if you want to read first before installing.

`pipx install openbusiness && openbusiness config`

MIT. Feedback welcome — especially: which agent's prompt would you rewrite first?
