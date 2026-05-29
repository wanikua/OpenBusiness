---
title: "I almost copied the multi-agent debate pattern. Here's why I went linear instead."
published: false
description: "Building OpenBusiness, an evidence-first business-model research CLI: why business analysis isn't a vote, how to make an LLM separate facts from guesses, and why unit economics should never run inside the model."
tags: ai, python, opensource, llm
cover_image:
---

> **How to publish:** paste this into a new [dev.to](https://dev.to) post. Set
> `published: true`, and upload `promo/images/report-preview.png` as the cover
> image (the `cover_image:` field). Same body works on Hashnode and Medium.

I built [OpenBusiness](https://github.com/wanikua/OpenBusiness), an open-source
CLI that turns a company name + domain into a business-model report from public
evidence. The interesting parts weren't the prompts — they were three design
decisions I had to argue myself out of.

## 1. Business analysis isn't a vote, so I dropped the debate

The obvious template for a multi-agent analysis tool right now is
[TradingAgents](https://github.com/TauricResearch/TradingAgents): bull agent,
bear agent, they debate, a judge converges on buy/sell. It's a great fit for
trading because there *is* a decision to converge on.

I almost copied it. Then I realized a business-model teardown has no buy/sell
output — it's a **structured decomposition**, not a verdict. Debate is the wrong
primitive when there's nothing to vote on; you'd just get two agents arguing
toward a midpoint that no one asked for.

So the pipeline is linear: 9 analyst agents in series, each adding one section.

```
evidence collector → JTBD → value prop → GTM → unit economics
  → moat → business-model-canvas synthesizer → assumption stress test → finalizer
```

The "what could be wrong here" signal that the debate was supposed to produce
comes instead from a dedicated **stress-test agent** at the end — cheaper, more
reproducible, and far easier to debug than emergent disagreement.

## 2. The whole point is separating facts from guesses

The failure mode of one-shot LLM company analysis is confident invention: ask
for Notion's churn and you'll get a number that looks sourced and isn't.

So every claim in the report carries a tag:

- `[VERIFIED:url]` — sourced from collected evidence
- `[INFERRED]` — the model's reasoning from context, labeled as such
- `[MISSING]` — couldn't verify; flagged instead of hidden

The system prompt forbids unlabeled claims, and the few-shot examples mix all
three so the model sees the distinction it's supposed to make. That tag is the
product.

## 3. The LLM never does the arithmetic

Unit economics (LTV, CAC, payback, lifetime) is a plain Python function
(`calculate_unit_economics` in `openbusiness/tools/`), not an LLM call. The
analyst's job is only to populate inputs *with their tags*:

```
arpu:          12.00  [VERIFIED:notion.so/pricing]
monthly_churn: 0.04   [INFERRED: typical SMB PLG]
cac:           150     [INFERRED: PLG blended estimate]
```

…and the function does the math, propagating the labels:

```
LTV:      $240.00  [VERIFIED:calculation — $12 × 25 months × 80% margin]
LTV/CAC:  1.6x
```

This kills the failure mode where a model confidently multiplies the wrong two
numbers in an LTV formula.

## What it actually produces

Here's the Notion sample (it's in [`examples/`](https://github.com/wanikua/OpenBusiness/tree/master/examples)
in the repo). Modeled LTV/CAC came out at **1.6x** — below the healthy 3x
benchmark. The useful part is the stress test, which ranks assumptions by how
much the conclusion moves when each is wrong:

> If actual monthly churn is **6%** instead of the inferred 4%, LTV drops to
> $160 and LTV/CAC falls to **1.07x** — unsustainable. If churn is **2%**
> (content lock-in works), LTV/CAC hits **3.2x** — healthy.

Same company, one assumption, opposite conclusions. That's the question the
report is built to surface: not "what is the number," but "which assumption
changes the story."

## A few implementation notes

- **Evidence is collected once, up front.** The collector dumps Tavily search,
  Firecrawl scrapes, and SEC EDGAR facts into one evidence pack; all 9 analysts
  read from it. Reproducible (same pack → same report) and cheaper (one set of
  retrieval calls, not nine).
- **Two model tiers.** Small models (mini / Haiku) for the analyst sections, a
  stronger model for synthesis + stress test. Full reports land around
  $0.10–$0.40 instead of $2–$5 on the strong model throughout.
- **Tag drift is real on smaller models.** In spot checks, long synthesis
  outputs started dropping evidence tags past ~1.5–2k tokens on some local-class
  models. (No formal eval harness yet — that's an open contribution.)

## Try it

```bash
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so --language en
```

Bring your own OpenAI, Anthropic, or DeepSeek key. Tavily and Firecrawl are
optional (without them the report leans more on `[INFERRED]`).

It's MIT, bilingual (en/zh), and I'd genuinely value feedback on where the
reasoning still over-infers from thin evidence:
**https://github.com/wanikua/OpenBusiness**

Which agent's prompt would you rewrite first?
