# r/LocalLLaMA — OpenBusiness

## Title

`Long synthesis outputs kept dropping evidence tags after ~1.5–2k tokens on Llama 3.1 70B`

## Body

The failure mode: long synthesis outputs would start clean, then drop evidence tags halfway through.

In my spot checks, Llama 3.1 70B started drifting around ~1.5–2k output tokens. Qwen 2.5 72B held longer, around ~2.5k tokens, then also started omitting tags or blending inferred claims into sourced ones. Mistral Large 2 did better than those local-ish options but still needed more prompt pressure than GPT-4o or Claude Sonnet 4.

I have not built an eval harness yet — quality assessment is spot checks. Treat these as working notes, not benchmark results.

The project is OpenBusiness: a CLI that creates a first-pass business model report from public evidence and tags claims 🟢 verified / 🟡 inferred / 🔴 missing. Repo: https://github.com/wanikua/OpenBusiness

The Notion sample is the concrete test case:

- Modeled LTV/CAC: 1.6x
- If monthly churn is 6% instead of inferred 4%: LTV/CAC → 1.07x
- If churn is 2%: LTV/CAC → 3.2x

The interesting part is not the business report. It's whether the model can keep evidence labels attached across a long, structured synthesis.

**1. Linear pipeline, no debate.**

The obvious inspiration was TradingAgents (multi-agent bull/bear debate → buy/sell vote). I almost copied it. Then I realized: business analysis output isn't a vote, it's a structured decomposition. Debate is the wrong primitive when there's no decision to converge on.

So the flow is 9 agents in series: Evidence Collector → JTBD → Value Prop → GTM → Unit Econ → Moat → Canvas Synthesizer → Stress Tester → Finalizer. Each one takes the accumulated state and adds a section.

The output about which assumptions break the analysis comes from a dedicated Stress Tester agent at the end, not from agent disagreement. Cheaper, more reproducible, easier to debug.

**2. Tag-each-claim prompting.**

The hardest prompt-engineering problem was getting the model to distinguish facts from inferences. The output convention:

```
🟢 [VERIFIED:url] for sourced claims
🟡 [INFERRED] for model inference from context
🔴 [MISSING] for things we couldn't verify but should flag
```

System prompt explicitly forbids unlabeled claims. Two-shot examples include mixed evidence so the model sees the distinction.

Model notes from spot checks:

- GPT-4o: best adherence in long final reports.
- Claude Sonnet 4: strong synthesis and stress-test reasoning.
- Claude Haiku 4.5: good for constrained analyst sections, weaker for final synthesis.
- Llama 3.1 70B: tag drift appeared around ~1.5–2k output tokens.
- Qwen 2.5 72B: tag drift appeared around ~2.5k output tokens.
- Mistral Large 2: better than Llama/Qwen in my runs, still not as consistent as GPT-4o/Sonnet for long reports.

**3. Pure-math tools beat LLM calculation.**

Unit economics (LTV, CAC, breakeven, lifetime months) is a Python function, not an LLM call. The analyst's job is to populate inputs *with tags* — "monthly_churn: 0.04 [INFERRED]", "arpu: 12.00 [VERIFIED:notion.so/pricing]" — and then `calculate_unit_economics(...)` does the multiplication.

The tag on each input propagates to the output: "LTV: $240 [VERIFIED:calculation — $12 × 25 × 0.80]".

This removes the failure mode where the model confidently outputs the wrong product in an LTV calculation.

**4. Two-tier model routing.**

- **Analyst tier** (Evidence, JTBD, Value Prop, GTM, Moat): gpt-4o-mini, Claude Haiku 4.5, or similar smaller model. Cheap, fast, constrained output.
- **Synthesis tier** (Canvas Synthesizer, Stress Tester): GPT-4o, Claude Sonnet 4, or another stronger model. These need long-context reasoning and counterfactual chains.

Result: ~$0.10–$0.40 per full report instead of ~$2–$5 if I run everything on the stronger model. In spot checks, quality drop on the analyst tier was small because the prompts and evidence pack carry most of the work.

**5. Evidence is pulled before any analyst runs.**

The Evidence Collector runs first and dumps everything into a markdown evidence pack (Tavily search results, Firecrawl page scrapes, SEC EDGAR financials for public companies). Every downstream analyst reads from this pack instead of doing its own retrieval.

Two benefits: (a) reproducibility — same evidence pack → same report; (b) cost — one set of retrieval calls, not nine.

**Stack:**

- LangGraph for the pipeline wiring
- OpenAI, Anthropic, or DeepSeek via config/env var
- Tavily / Firecrawl / SEC EDGAR tools in `openbusiness/tools/`
- Rich for the CLI UX

**Tried but discarded:**

- Llama 3.1 70B and Qwen 2.5 72B for long final synthesis — tag drift was too frequent at temperature 0. Might be salvageable with structured output / JSON mode, but I did not push hard enough on it. Open to PRs if anyone wants to.
- Self-correction loop (run synthesizer, then a critic, then re-synthesize) — added 3x latency for marginal quality gain.

**Limitations:**

- No eval harness yet; quality notes above are spot checks.
- Private companies → fragile reports (no SEC, lots of 🟡 and 🔴).
- Reports take 2–4 minutes.
- No streaming output yet (it batches per agent).

Install if you want to play:
```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

Full Notion sample report in `examples/`. MIT.

Happy to dig into the prompts or the LangGraph wiring in comments — and especially interested if anyone has gotten the tag convention to hold on 7B-class models.
