# r/SideProject — OpenBusiness

## Title

`Built a CLI that showed Notion at 1.6x LTV/CAC, then stress-tested the churn assumption`

## Body

The sample that finally made the project click was Notion.

OpenBusiness modeled LTV/CAC at **1.6x** — below the healthy 3x benchmark. Then the stress tester changed one assumption:

> *"If actual monthly churn is 6% instead of the inferred 4%, LTV/CAC → 1.07x, unsustainable. If churn is 2%, LTV/CAC → 3.2x, healthy."*

That is the output I wanted: not a polished company summary, but a report that shows which assumption can flip the conclusion.

**OpenBusiness** takes a company name and domain, gathers public evidence, and produces a business model canvas where each line is tagged:

- 🟢 `[VERIFIED:url]` — sourced from evidence
- 🟡 `[INFERRED]` — model guess from context
- 🔴 `[MISSING]` — couldn't verify, flagged anyway

It's a 9-agent linear pipeline: evidence collector → JTBD → value prop → GTM → unit economics → moat → canvas synthesizer → assumption stress tester → finalizer. Built on LangGraph with OpenAI, Anthropic, and DeepSeek support.

**The design decision I had to make early:** the obvious inspiration was [TradingAgents](https://github.com/TauricResearch/TradingAgents), which uses a bull/bear debate to produce a buy/sell vote. I almost copied that structure. Then I realized business model analysis isn't a vote — it's a structured decomposition. Debate is the wrong primitive when there's no decision to make. So I went linear and used a stress tester instead of a debate to surface fragile assumptions.

**What's working:**

- The 🟢/🟡/🔴 tag convention. Models follow it much better when the prompt includes mixed examples.
- Unit economics done in Python, not LLM. The analyst populates inputs with tags and a `unit_econ.py` function does the math.
- Two-tier model routing — mini/haiku for analysts, stronger model for the synthesizer. Cost dropped to ~$0.10–$0.40/report.

**What's not working yet:**

- Comparison mode. I want `openbusiness compare Notion Coda` to produce a side-by-side, but the prompt for "what's different in a meaningful way" is still bad.
- HTML report with collapsible evidence trails. Markdown is fine but the evidence trail bloats the report.
- Private companies still produce thin reports. Without SEC filings, you're stuck inferring most of the unit economics.

Repo (MIT, samples in `output/`): https://github.com/wanikua/OpenBusiness

Install:
```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

Bring your own LLM key. Tavily and Firecrawl are optional but the report gets more 🟡 without them.

Happy to talk through the prompts, the LangGraph wiring, or the two-tier cost work if anyone's building something similar.
