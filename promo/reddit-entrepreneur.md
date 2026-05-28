# r/Entrepreneur — OpenBusiness

## Title

`Notion looked like 1.6x LTV/CAC — then one churn assumption changed the whole model`

## Body

I ran a first-pass report on Notion and got the kind of answer I wish more founder decks admitted.

Modeled LTV/CAC: **1.6x** — below the healthy 3x benchmark. The stress test then showed why the conclusion was fragile:

> *"If actual monthly churn is 6% instead of the inferred 4%, LTV drops to $160, LTV/CAC → 1.07x — unsustainable. If churn is 2% (content lock-in works), LTV/CAC → 3.2x — healthy."*

That is the real question: not "what is the number?" but "which assumption changes the story?"

So I built **OpenBusiness**, an open-source CLI that creates a business model report from public evidence and tags each claim:

- 🟢 verified (sourced, citable)
- 🟡 inferred (model guess from context)
- 🔴 missing (couldn't verify — flagged, not hidden)

You point it at a company name + domain. It pulls evidence (Tavily search, Firecrawl scrape, SEC EDGAR for public companies), runs 9 analyst agents (JTBD, value prop, GTM, unit economics, moat, etc.), then synthesizes a business model canvas with evidence labels.

**The part most people find useful is the Assumption Stress Tester.**

It ranks the assumptions by how much the report changes when each one is wrong. In the Notion sample, churn, ARPU, and CAC matter far more than the rest of the narrative. That's what investors should ask about, and what founders should know before they put numbers in a deck.

**Why it matters for founders:**

1. **Run it on your own company.** It separates what is verified from what is assumed in your model. Better to find the weak assumptions before a board call.
2. **Run it on competitors.** You get a structured first-pass report without spending 8 hours gathering notes.
3. **Run it before a fundraise.** The stress tester output gives you the questions a sharp investor is likely to ask.

**What it isn't:**

- Not a market research tool. It analyzes business *models*, not market sizes.
- Not a fortune teller for private-company financials. If actual ARPU isn't public, it'll mark it 🔴 instead of inventing a number.
- Reports cost $0.10–$0.40 in API calls and take 2–4 minutes.

Bring your own OpenAI, Anthropic, or DeepSeek key. Tavily + Firecrawl are optional but recommended (both free tiers are enough).

```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

MIT licensed. Sample reports for Notion, Vercel, and OpenAI are in `output/` if you want to read them before installing.

→ https://github.com/wanikua/OpenBusiness

Curious what you'd run it on — and which assumption changes the report.
