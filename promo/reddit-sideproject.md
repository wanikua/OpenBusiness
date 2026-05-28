# r/SideProject — OpenBusiness

## Title

`Built a CLI that reverse-engineers any company's business model and tags every claim 🟢 verified / 🟡 inferred / 🔴 missing`

## Body

Background: I'd been reading a lot of "AI does business analysis" posts and every output looked the same — a confident-sounding PDF where you couldn't tell which numbers were real and which were the LLM making things up. So I built a tool that's structurally incapable of doing that.

**OpenBusiness** takes a company name and produces a full business model canvas where every single line is tagged:

- 🟢 `[VERIFIED:url]` — sourced from real evidence
- 🟡 `[INFERRED]` — LLM guess from context
- 🔴 `[MISSING]` — couldn't verify, flagged anyway

It's a 9-agent linear pipeline: evidence collector → JTBD → value prop → GTM → unit economics → moat → canvas synthesizer → assumption stress tester → finalizer. Built on LangGraph + OpenAI/Anthropic.

**The design decision I had to make early:** the obvious inspiration was [TradingAgents](https://github.com/TauricResearch/TradingAgents), which uses a bull/bear debate to produce a buy/sell vote. I almost copied that structure. Then I realized business model analysis isn't a vote — it's a structured decomposition. Debate is the wrong primitive when there's no decision to make. So I went linear and used a stress tester instead of a debate to surface fragile assumptions.

**What's working:**

- The 🟢/🟡/🔴 tag convention. Models actually respect it once you put it in the prompt with examples.
- Unit economics done in Python, not LLM. LLMs can't multiply reliably, so I let the analyst populate inputs (with tags) and a `unit_econ.py` function does the math.
- Two-tier model routing — mini/haiku for analysts, deep model for the synthesizer. Cost dropped to ~$0.10–$0.40/report.

**What's not working yet:**

- Comparison mode. I want `openbusiness compare Notion Coda` to produce a side-by-side, but the prompt for "what's different in a meaningful way" is still bad.
- HTML report with collapsible evidence trails. Markdown is fine but the evidence trail bloats the report.
- Private companies still produce thin reports. Without SEC filings, you're stuck inferring most of the unit economics.

**Sample output from running it on Notion:**

It told me LTV/CAC = 1.6x (warning), then the stress tester said: *"If actual monthly churn is 6% instead of the inferred 4%, LTV/CAC → 1.07x, unsustainable. If churn is 2%, LTV/CAC → 3.2x, healthy."* That kind of "here's the load-bearing assumption" output is the part I'm most happy with.

Repo (MIT, samples in `output/`): https://github.com/wanikua/OpenBusiness

Install:
```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

Bring your own LLM key. Tavily and Firecrawl are optional but the report gets more 🟡 without them.

Happy to talk through the prompts, the LangGraph wiring, or the two-tier cost optimization if anyone's building something similar.
