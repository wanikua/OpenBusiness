# r/Entrepreneur — OpenBusiness

## Title

`I built a tool that audits your business model the way a competitor would — and flags every assumption that's load-bearing`

## Body

I kept seeing founder decks where the LTV slide was suspiciously precise. $487 LTV. 4.2% monthly churn. CAC payback in 9 months. The numbers were always either pulled out of a model with one giant unverified assumption, or just made up. The honest answer for a private company is "we don't actually know" — but nobody says that.

So I built **OpenBusiness**, an open-source CLI that reverse-engineers any company's business model and is *forced* to tag every single claim:

- 🟢 verified (sourced, citable)
- 🟡 inferred (LLM guess from context)
- 🔴 missing (couldn't verify — flagged, not hidden)

You point it at a company name + domain. It pulls real evidence (Tavily search, Firecrawl scrape, SEC EDGAR for public companies), runs 9 analyst agents (JTBD, value prop, GTM, unit economics, moat, etc.), then synthesizes a full business model canvas with every cell tagged.

**The part most people find surprising is the Assumption Stress Tester.**

I ran it on Notion. The unit economics said LTV/CAC = 1.6x — below the healthy 3x benchmark. Borderline. But the stress tester then told me:

> *"4% monthly churn is the load-bearing assumption. If actual churn is 6% (not uncommon for pure PLG SMBs), LTV drops to $160, LTV/CAC → 1.07x — unsustainable. If churn is 2% (content lock-in works), LTV/CAC → 3.2x — healthy."*

It ranked five assumptions by how badly the canvas collapses when each one is wrong. That's the thing investors should be asking you about your own deck, and rarely do.

**Why it matters for founders:**

1. **Run it on your own company.** It's brutally honest about what's verified vs. assumed in your model. Cheaper than realizing it on a board call.
2. **Run it on competitors.** You get a structured teardown without spending 8 hours on it.
3. **Run it before a fundraise.** The stress tester output is basically a pre-cooked list of the questions a sharp investor will hit you with.

**What it isn't:**

- Not a market research tool. It analyzes business *models*, not market sizes.
- Not a fortune teller for private-company financials. If actual ARPU isn't public, it'll mark it 🔴 instead of inventing a number. That's the whole point.
- Reports cost $0.10–$0.40 in API calls and take 2–4 minutes.

Bring your own OpenAI or Anthropic key. Tavily + Firecrawl are optional but recommended (both free tiers are enough).

```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

MIT licensed. Sample reports for Notion, Vercel, and OpenAI are in `output/` if you want to read them before installing.

→ https://github.com/wanikua/OpenBusiness

Curious what you'd run it on — and what the report tells you that you didn't already know.
