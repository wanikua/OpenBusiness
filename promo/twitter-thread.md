# X / Twitter Launch Thread — OpenBusiness

> Post the hook tweet with the **demo-report.svg** rendered as PNG attached. Each tweet ≤ 280 chars.

---

**1/**
Most "AI business analysis" tools fabricate confident prose.

I built one that tags every single claim:

🟢 verified  ·  🟡 inferred  ·  🔴 missing

You can see at a glance which numbers are real and which are guesses.

It's called OpenBusiness. Free, open source, MIT.

🧵 ↓

---

**2/**
Input: a company name.

Output: a structured business model canvas + unit economics + moat analysis + a "what-breaks-the-canvas" stress test.

Every line is tagged. No more LLM laundering an inference as a fact.

[ATTACH: assets/demo-report.svg]

---

**3/**
I ran it on Notion. Here's what it told me:

LTV/CAC = 1.6x

⚠️ Below the healthy 3x benchmark.

Then it told me *why* — and what assumption is load-bearing.

---

**4/**
"If actual monthly churn is 6% instead of 4%, LTV drops to $160, LTV/CAC → 1.07x. Unsustainable."

"If churn is 2%, LTV jumps to $480, LTV/CAC → 3.2x. Healthy."

This is the part I haven't seen elsewhere. The model says which assumption, if wrong, kills the analysis.

---

**5/**
9-agent linear pipeline. No bull/bear debate.

🔍 Evidence Collector (Tavily + Firecrawl + SEC EDGAR)
👥 JTBD → 💎 Value Prop → 🚀 GTM
💰 Unit Econ (pure Python math, not LLM)
🛡️ Moat → 🧱 Canvas → 🔬 Stress Test → 📝 Final

Inspired by TradingAgents but business ≠ a buy/sell vote.

---

**6/**
Design choices that matter:

• Evidence pulled BEFORE any analyst runs
• Unit economics is a Python function — LLMs can't multiply
• Two LLM tiers: mini/haiku for analysts, deep model for synthesis (≈10x cheaper than running everything on a frontier model)
• Every claim tagged

---

**7/**
Honest about what it can't do:

It won't get you a verified ARPU when the company is private. It'll tell you that's missing and flag it 🔴, instead of inventing a number.

That's the entire point.

---

**8/**
Install:

```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

Bring your own OpenAI or Anthropic key. Tavily + Firecrawl are optional (you get more 🟡 without them).

---

**9/**
Sample reports already in the repo for Notion, Vercel, OpenAI.

Clone, run it on a company you care about, and tell me what surprised you.

→ https://github.com/wanikua/OpenBusiness

⭐ if useful.
