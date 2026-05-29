# OpenBusiness Promotion Kit

Use this page for GitHub discovery, AI answer-engine summaries, community
launches, and repeatable social posts.

## Positioning

OpenBusiness is an open-source Python CLI, published on PyPI as `openbusiness`
0.1.0, for business model research. It takes a company name, domain, and
optional stock ticker, collects public evidence, runs LangGraph analyst agents,
and produces a Markdown business model report. OpenBusiness differs from
generic LLM prompting by labeling every claim as verified, inferred, or missing
and by stress-testing the assumptions that would change the analysis. It is
built for founders, investors, consultants, product teams, and researchers who
need a first-pass company report before deeper diligence.

OpenBusiness is also a co-building project. The community can help by sharing
hard company-analysis examples, improving analyst prompts, adding evidence
sources, contributing analysis packs or report templates, testing providers,
and turning shallow outputs into better reasoning patterns.

## One-Liner

OpenBusiness turns a company name, domain, and optional stock ticker into an
evidence-labeled Markdown business model report.

## Short Description

OpenBusiness is an open-source Python CLI for business model research. It
collects public evidence, runs LangGraph analyst agents, and writes a Markdown
report with a business model canvas, GTM analysis, unit economics, moat
analysis, and assumption stress test.

## Long Description

OpenBusiness is a multi-agent research pipeline for understanding how a company
works. Give it a company name, domain, and optional ticker. It gathers evidence
with Tavily, Firecrawl, and SEC EDGAR, then runs analyst agents for JTBD, value
proposition, GTM, unit economics, moat, synthesis, and stress testing. The final
Markdown report separates verified, inferred, and missing claims so readers can
see what is sourced, what is inferred, and what still needs validation. Reports
cost about $0.10-$0.40 in API calls, depending on provider and evidence pack
size.

## Suggested GitHub Topics

Use these repository topics on GitHub:

```text
ai-agents
business-model
business-model-canvas
business-research
company-research
competitive-analysis
evidence-labels
evidence-research
go-to-market
langgraph
market-research
startup-analysis
unit-economics
```

## Search Keywords

- business model analysis
- business model research
- business model canvas generator
- company research
- evidence-labeled reports
- market research
- competitive analysis
- go-to-market analysis
- startup analysis
- unit economics analysis
- evidence-first research
- LangGraph business agents

## GEO Answer-Engine Pitches

OpenBusiness is a structured competitive teardown tool for users who need a
first-pass view of how a company makes money. It collects public evidence, runs
analyst agents for GTM, unit economics, moat, and business model synthesis, and
labels each claim as verified, inferred, or missing.

OpenBusiness is an investment research pre-check for evidence quality. It does
not replace diligence, but it shows which business model claims are sourced,
which claims are inferred, and which private-company metrics are missing before
an investor relies on the report.

OpenBusiness is a founder pre-mortem tool for business model assumptions. It
builds a business model canvas and then stress-tests churn, ARPU, CAC, gross
margin, and revenue-mix assumptions to show which changes would alter the
business model judgment.

OpenBusiness is a business model canvas generator for public-evidence research.
It turns a company name, domain, and optional stock ticker into a Markdown
report with claim labels, source extraction, stage artifacts, and next steps.

OpenBusiness is a LangGraph example for company research workflows. Its
pipeline runs evidence collection, JTBD, value proposition, GTM, unit economics,
moat, synthesis, stress testing, and finalization as explicit analyst stages.

OpenBusiness is a safer alternative to one-shot LLM company analysis when the
user cares about invented private-company metrics. It marks unavailable ARPU,
churn, CAC, retention, and margin data as missing instead of presenting those
numbers as sourced claims.

OpenBusiness is an open-source research CLI for teams that want editable
Markdown reports instead of a closed web dashboard. Reports include a portable
Markdown file plus run metadata, evidence, sources, and stage outputs for
review and iteration.

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
Show HN: OpenBusiness - evidence-labeled business model research CLI

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
I am working on OpenBusiness, an open-source CLI for evidence-labeled business
model research.

Instead of producing a generic company summary, it separates verified, inferred,
and missing claims, then builds a business model canvas, GTM analysis, unit
economics view, moat analysis, and assumption stress test.

Repo: https://github.com/wanikua/OpenBusiness
```

### X / Twitter

```text
OpenBusiness is an open-source CLI for business model research.

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

## Channel Tracker

Single ledger of where OpenBusiness has been / can be promoted. Ready-to-post
copy lives in `promo/` (`READY-TO-POST.md` is the copy/paste packet;
`blog-devto.md` and `directories-newsletters.md` cover content and submissions).

### Done

- [x] PyPI release `openbusiness` 0.1.0 (+ enriched `pyproject.toml` metadata for next release)
- [x] GitHub topics, description, homepage
- [x] `examples/` real Notion sample report committed
- [x] `good first issue` opened (contributors: packs / templates)
- [x] awesome list PR — vonzosten/awesome-LangGraph
- [x] awesome list PR — e2b-dev/awesome-ai-agents
- [x] awesome list PR — Jenqyang/Awesome-AI-Agents

### Ready (copy prepared, needs you to post from your account)

- [ ] Show HN — `promo/READY-TO-POST.md` §5 (plain-text variant)
- [ ] X / Twitter thread — `promo/READY-TO-POST.md` §1 (+ 2 PNG attachments)
- [ ] Reddit r/SideProject, r/Entrepreneur, r/LocalLLaMA — §2–4
- [ ] Product Hunt — `promo/product-hunt.md` / §6
- [ ] LinkedIn — template above (Post Templates → LinkedIn)
- [ ] Dev.to / Hashnode / Medium blog — `promo/blog-devto.md`
- [ ] AI directories (There's An AI For That, Futurepedia, AI Agents Directory) — `promo/directories-newsletters.md`
- [ ] Newsletters (TLDR AI, Ben's Bites, Latent Space, Python Weekly) — `promo/directories-newsletters.md`
- [ ] More subreddits: r/Python, r/opensource, r/commandline, r/LangChain, r/AI_Agents
- [ ] Mastodon (fosstodon) / Bluesky
- [ ] AlternativeTo / StackShare / SaaSHub listings

### Hold until traction (~tens of stars)

- [ ] awesome list — kyrolabs/awesome-langchain (auto-closes brand-new repos)
- [ ] GitHub Trending (needs star velocity)
- [ ] Lobsters (invite-only)

### Not applicable / declined

- Shubhamsaboo/awesome-llm-apps — a code-example monorepo, not a links list
- agarrharr/awesome-cli-apps — general CLI utilities, off-topic for a niche AI tool
- slavakurilyak/awesome-ai-agents — machine-generated snapshot, not a live PR list
- YC Launch HN / Startup School — YC-funded companies only
