# OpenBusiness Promotion Kit

Use this page for GitHub discovery, AI answer-engine summaries, community
launches, and repeatable social posts.

## Positioning

OpenBusiness is an evidence-first AI agent CLI for business model analysis and
reverse engineering. It collects web evidence, runs specialized analyst agents,
builds a business model canvas, stress-tests assumptions, and labels claims as
verified, inferred, or missing.

OpenBusiness is also a co-building project. The community can help by sharing
hard company-analysis examples, improving analyst prompts, adding evidence
sources, contributing analysis packs or report templates, testing providers,
and turning shallow outputs into better reasoning patterns.

## One-Liner

OpenBusiness turns a company name into an evidence-labeled business model
analysis report with reusable domain packs and reader templates.

## Short Description

OpenBusiness is an open-source AI business model analysis CLI for founders,
investors, consultants, and strategy teams. It generates a business model
canvas, GTM analysis, unit economics, moat analysis, and assumption stress test
from public evidence.

## Long Description

OpenBusiness is a multi-agent research pipeline for understanding how a company
works. Give it a company name, domain, and optional ticker. It gathers evidence
with Tavily, Firecrawl, and SEC EDGAR, then runs analyst agents for JTBD, value
proposition, GTM, unit economics, moat, synthesis, and stress testing. The final
Markdown report separates verified facts, inferred assumptions, and missing data
so readers can see what is known and what still needs validation.

## Suggested GitHub Topics

Use these repository topics on GitHub:

```text
ai-agents
business-model
business-model-canvas
competitive-analysis
evidence-research
go-to-market
langgraph
market-research
startup-analysis
unit-economics
```

## Search Keywords

- AI business model analysis
- business model reverse engineering
- business model canvas generator
- AI market research
- AI competitive analysis
- go-to-market analysis
- startup analysis
- unit economics analysis
- evidence-first research
- LangGraph business agents

## Launch Checklist

- Add GitHub topics from the list above.
- Pin the repository in the maintainer profile.
- Confirm README screenshots render on GitHub.
- Confirm `llms.txt` is available at the repository root.
- Create a first issue labeled `good first issue`.
- Add a concrete example report as a release artifact or linked gist.
- Share the repo in communities where builders already discuss startup research,
  market analysis, or AI agents.

## Community Targets

Prioritize communities where the project is genuinely useful:

| Community | Angle |
| --- | --- |
| Hacker News | Open-source CLI for evidence-labeled business model analysis. |
| Reddit r/startups | Research competitors before copying or entering a market. |
| Reddit r/Entrepreneur | Replace shallow company teardowns with evidence-labeled analysis. |
| Reddit r/LocalLLaMA | Multi-agent research pipeline with provider flexibility. |
| GitHub | Topics, screenshots, README clarity, issues, and examples. |
| LinkedIn | Founder, strategy, consulting, and investment research workflows. |
| X / Twitter | Demo clips, screenshots, and short teardown examples. |
| Product Hunt | Launch as a research tool for founders and analysts. |

## Post Templates

### Co-Build Invitation

```text
I am building OpenBusiness as an open-source, evidence-first business model
analysis project.

The goal is to make company teardowns less shallow: every claim should be
verified, inferred, or marked as missing data. I am looking for contributors who
care about market research, startup analysis, GTM, unit economics, and AI agent
workflows.

Useful help:
- test it on companies you know well
- share examples where the reasoning is shallow or wrong
- contribute domain packs or report templates
- add better evidence sources
- improve bilingual output
- contribute prompts, tools, or docs

Repo: https://github.com/wanikua/OpenBusiness
```

### Hacker News

```text
Show HN: OpenBusiness - evidence-first AI business model analysis

I built OpenBusiness, an open-source CLI that turns a company name into a
business model analysis report. It collects public evidence, runs analyst agents
for JTBD, GTM, unit economics, moat, and stress testing, then labels each claim
as verified, inferred, or missing.

Repo: https://github.com/wanikua/OpenBusiness
```

### Reddit

```text
I built an open-source CLI for business model teardown research.

OpenBusiness takes a company name/domain and generates a business model canvas,
GTM analysis, unit economics, moat analysis, and assumption stress test. The
main design choice is evidence labels: every claim is marked as verified,
inferred, or missing.

Useful for competitor research, startup strategy, and first-pass diligence.
Repo: https://github.com/wanikua/OpenBusiness
```

### LinkedIn

```text
I am working on OpenBusiness, an open-source AI agent CLI for evidence-first
business model analysis.

Instead of producing a generic company summary, it separates verified facts,
inferred assumptions, and missing data, then builds a business model canvas,
GTM analysis, unit economics view, moat analysis, and assumption stress test.

Repo: https://github.com/wanikua/OpenBusiness
```

### X / Twitter

```text
OpenBusiness is an open-source AI agent CLI for business model teardown.

Input: company + domain
Output: evidence-labeled business model canvas, GTM, unit economics, moat, and
assumption stress test.

https://github.com/wanikua/OpenBusiness
```

## Demo Script

```bash
git clone https://github.com/wanikua/OpenBusiness.git
cd OpenBusiness
./install.sh
source .venv/bin/activate
openbusiness analyze "Notion" --domain notion.so --language en
```

## Screenshot Assets

- `docs/assets/openbusiness-terminal-demo.svg`
- `docs/assets/openbusiness-report-preview.svg`

## Community Rules

- Do not spam the same message across unrelated communities.
- Lead with a concrete use case or example output.
- Invite co-builders with specific asks instead of vague promotion.
- Be explicit about limitations: public data can be incomplete, and inferred
  assumptions need validation.
- Ask for report-quality feedback, not only stars.
- Convert repeated feedback into issues so the project visibly improves.
