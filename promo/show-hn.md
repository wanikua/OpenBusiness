# Show HN Post — OpenBusiness

## Title

`Show HN: OpenBusiness – Notion LTV/CAC was 1.6x until churn changed`

(70 chars. Avoid "AI-powered" / "revolutionary"; HN allergic to both.)

## URL field

`https://github.com/wanikua/OpenBusiness`

## Body

I ran OpenBusiness on Notion and the useful part was not the canvas. It was the stress test: modeled LTV/CAC came out to 1.6x, below the healthy 3x benchmark. If inferred monthly churn moves from 4% to 6%, LTV drops to $160 and LTV/CAC falls to 1.07x. If churn is 2%, LTV jumps to $480 and LTV/CAC reaches 3.2x.

That is the problem I wanted the tool to expose: which assumption changes the conclusion?

OpenBusiness is an open-source CLI that builds a first-pass business model report from public evidence. It tags claims as:

- 🟢 `[VERIFIED:url]` — sourced from evidence (Tavily search, Firecrawl scrape, SEC EDGAR)
- 🟡 `[INFERRED]` — model inference from context
- 🔴 `[MISSING]` — data could not be verified and affects confidence

Pipeline is 9 agents in a linear flow (LangGraph). Inspired by TradingAgents, but I deliberately did not copy the bull/bear debate. Business model output is a decomposition, not a buy/sell vote.

Two implementation details that took longest to get right:
1. Unit economics is a Python function, not an LLM call. The analyst populates inputs with tags, then the math runs.
2. Two-tier model routing: mini/haiku for the analysts, a stronger model for the synthesizer and stress tester. Full reports cost about $0.10–$0.40 depending on provider.

Providers: OpenAI, Anthropic, and DeepSeek. Tavily and Firecrawl are optional, but without live retrieval the report depends more on inference and should be treated as weaker.

Limitations: it cannot verify private-company financials when the company does not publish them, so private companies get more 🟡/🔴 tags. Reports take 2–4 minutes. Quality depends heavily on the evidence available.

Sample reports for Notion, Vercel, and OpenAI are in `output/` if you want to read before installing.

`pipx install openbusiness && openbusiness config`

MIT. Feedback welcome — especially: which agent's prompt would you rewrite first?
