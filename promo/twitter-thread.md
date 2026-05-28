# X / Twitter Launch Thread — OpenBusiness

> Post the hook tweet with the **openbusiness-report-preview.svg** rendered as PNG attached. Each tweet ≤ 280 chars.

---

**1/**
I ran OpenBusiness on Notion.

It modeled LTV/CAC at 1.6x — below the healthy 3x benchmark.

Then it showed the dangerous part:

6% monthly churn → 1.07x
2% monthly churn → 3.2x

Same company, different churn assumption, totally different story.

🧵 ↓

---

**2/**
OpenBusiness is a free, open-source CLI that turns public evidence into a first-pass business model report.

Every claim is tagged:

🟢 verified  ·  🟡 inferred  ·  🔴 missing

It separates facts from guesses.

[ATTACH: docs/assets/openbusiness-report-preview.svg]

---

**3/**
Input: a company name + domain.

Output: business model canvas, unit economics, moat analysis, and an assumption stress test.

Notion example:

LTV/CAC = 1.6x

⚠️ Below the healthy 3x benchmark.

---

**4/**
"If actual monthly churn is 6% instead of 4%, LTV drops to $160, LTV/CAC → 1.07x. Unsustainable."

"If churn is 2%, LTV jumps to $480, LTV/CAC → 3.2x. Healthy."

That churn estimate is the assumption that changes the whole report.

---

**5/**
9-agent linear pipeline. No bull/bear debate.

🔍 Evidence Collector (Tavily + Firecrawl + SEC EDGAR)
👥 JTBD → 💎 Value Prop → 🚀 GTM
💰 Unit Econ (pure Python math, not LLM)
🛡️ Moat → 🧱 Canvas → 🔬 Stress Test → 📝 Final

Business analysis is decomposition, not a vote.

---

**6/**
Design choices that matter:

• Evidence pulled before analysts run
• Unit economics is a Python function
• Two LLM tiers: mini/haiku for analysts, stronger model for synthesis
• Provider support: OpenAI, Anthropic, DeepSeek
• Each claim tagged

---

**7/**
Honest about what it can't do:

It won't get you verified ARPU when a private company doesn't publish it.

It marks that 🔴 missing instead of inventing a number.

That's the point.

---

**8/**
Install:

```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

Bring your own OpenAI, Anthropic, or DeepSeek key. Tavily + Firecrawl are optional (you get more 🟡 without them).

---

**9/**
Sample reports already in the repo for Notion, Vercel, OpenAI.

Clone, run a first-pass report from public evidence, and tell me which assumption changed the story.

→ https://github.com/wanikua/OpenBusiness

⭐ if useful.
