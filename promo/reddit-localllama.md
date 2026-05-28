# r/LocalLLaMA — OpenBusiness

## Title

`9-agent linear pipeline for business model analysis — tag-every-claim prompting + two-tier model routing for ~10x cost reduction`

## Body

Sharing the architecture of a side project that I think r/LocalLLaMA will appreciate the design notes on more than the product itself. The product is OpenBusiness — a CLI that reverse-engineers any company's business model and tags every claim 🟢 verified / 🟡 inferred / 🔴 missing. Repo: https://github.com/wanikua/OpenBusiness

The interesting bits aren't the agents — they're the design choices I made *against* the obvious patterns.

**1. Linear pipeline, no debate.**

The obvious inspiration was TradingAgents (multi-agent bull/bear debate → buy/sell vote). I almost copied it. Then I realized: business analysis output isn't a vote, it's a structured decomposition. Debate is the wrong primitive when there's no decision to converge on. So the flow is just 9 agents in series: Evidence Collector → JTBD → Value Prop → GTM → Unit Econ → Moat → Canvas Synthesizer → Stress Tester → Finalizer. Each one takes the accumulated state and adds a section.

The "interesting" output (which assumptions, if wrong, break the analysis) comes from a dedicated Stress Tester agent at the end, not from agent disagreement. Cheaper, more reproducible, easier to debug.

**2. Tag-every-claim prompting.**

The hardest prompt-engineering problem was getting the model to actually distinguish facts from inferences. The solution was a strict output convention:

```
🟢 [VERIFIED:url] for sourced claims
🟡 [INFERRED] for LLM inference from context
🔴 [MISSING] for things we couldn't verify but should flag
```

System prompt explicitly forbids unlabeled claims. Two-shot examples in the prompt with deliberately-mixed evidence so the model sees the distinction. Empirically, all of GPT-4-class, Claude 3.5+, and even Haiku respect the convention if you include the examples. Smaller models (7B-13B) drift after ~2k tokens of output and start dropping tags.

**3. Pure-math tools beat LLM calculation.**

Unit economics (LTV, CAC, breakeven, lifetime months) is a Python function, not an LLM call. The analyst's job is to populate inputs *with tags* — "monthly_churn: 0.04 [INFERRED]", "arpu: 12.00 [VERIFIED:notion.so/pricing]" — and then `unit_econ_calc(...)` does the multiplication. The tag on every input propagates to the output: "LTV: $240 [VERIFIED:calculation — $12 × 25 × 0.80]".

This eliminates the "model confidently outputs the wrong product" failure mode that kills LTV calculations in pure-prompt approaches.

**4. Two-tier model routing.**

- **Analyst tier** (Evidence, JTBD, Value Prop, GTM, Moat): gpt-4o-mini or Claude Haiku. Cheap, fast, the structure of their outputs is constrained enough that a smaller model is fine.
- **Synthesis tier** (Canvas Synthesizer, Stress Tester): gpt-4o or Claude Sonnet. These need long-context reasoning and the stress tester especially needs to do counterfactual chains.

Result: ~$0.10–$0.40 per full report instead of ~$2–$5 if I ran everything on the deep model. Tested both — quality drop on the analyst tier is barely perceptible because the prompts and the evidence pack carry most of the work.

**5. Evidence is pulled before any analyst runs.**

The Evidence Collector runs first and dumps everything into a markdown "evidence pack" (Tavily search results, Firecrawl page scrapes, SEC EDGAR financials for public companies). Every downstream analyst reads from this pack instead of doing its own retrieval. Two benefits: (a) reproducibility — same evidence pack → same report; (b) cost — one set of retrieval calls, not nine.

**Stack:**

- LangGraph for the pipeline wiring (overkill for linear flow, but I like the state model)
- OpenAI or Anthropic via env var swap
- Tavily / Firecrawl / SEC EDGAR adapters in `openbusiness/dataflows/`
- Rich for the CLI UX

**Tried but discarded:**

- Local models (Llama 3.1 70B, Qwen 2.5 72B) — tag drift was too bad on the long synthesis outputs even at temperature 0. Might be salvageable with structured output / JSON mode, but I didn't push hard enough on it. Open to PRs if anyone wants to.
- Self-correction loop (run synthesizer, then a critic, then re-synthesize) — added 3x latency for marginal quality gain.

**Limitations:**

- Private companies → fragile reports (no SEC, lots of 🟡 and 🔴)
- Reports take 2–4 minutes
- No streaming output yet (it batches per agent)

Install if you want to play:
```
pipx install openbusiness
openbusiness config
openbusiness analyze "Notion" --domain notion.so
```

Sample reports in `output/`. MIT.

Happy to dig into the prompts or the LangGraph wiring in comments — and especially interested if anyone's gotten the tag convention to hold on a 7B-class model.
