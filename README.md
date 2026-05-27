# OpenBusiness

> Evidence-first AI business model analysis and reverse engineering for founders,
> investors, consultants, and strategy teams.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-1f2937?style=flat-square)](https://www.langchain.com/langgraph)
[![Reports](https://img.shields.io/badge/Output-English%20%7C%20zh-0f766e?style=flat-square)](#bilingual-output)
[![License](https://img.shields.io/badge/License-MIT-black?style=flat-square)](#license)

OpenBusiness is an open-source AI agent CLI for business model analysis,
competitive research, market research, go-to-market strategy, unit economics,
and business model canvas generation. Give it a company name, domain, and
optional stock ticker; it collects evidence from the web, runs specialized
analyst agents, builds a structured business model canvas, stress-tests
assumptions, and labels each claim as verified, inferred, or missing.

It is inspired by [TradingAgents](https://github.com/TauricResearch/TradingAgents),
but OpenBusiness is not a bull-vs-bear debate system. Business model analysis
needs decomposition, evidence tracking, and assumption pressure-testing, not a
buy/sell vote.

![OpenBusiness terminal demo](docs/assets/openbusiness-terminal-demo.svg)

![OpenBusiness report preview](docs/assets/openbusiness-report-preview.svg)

## Highlights

- Multi-agent business analysis pipeline built with LangGraph.
- Evidence collection through Tavily search, Firecrawl scraping, and SEC EDGAR.
- Business model canvas output with explicit evidence labels.
- Bilingual report generation with `--language en` and `--language zh`.
- Provider support for OpenAI, Anthropic, and DeepSeek.
- Local config wizard with hidden API-key input and `0600` config permissions.
- Language-purity warnings when generated reports mix output languages.
- Pure Markdown reports that can be archived, edited, or shared directly.

## Use Cases

OpenBusiness is useful when you need a structured first-pass business model
research report before deeper diligence:

| Audience | Common question | OpenBusiness output |
| --- | --- | --- |
| Founders | What can I copy, avoid, or attack in this market? | GTM motion, value proposition, moat, and fatal weakness. |
| Investors | Is the company robust, plausible, fragile, or speculative? | Evidence-labeled thesis, assumptions, and stress test. |
| Consultants | How does this company actually make money? | Business model canvas, profit engine, and unit economics. |
| Product teams | Why do customers switch and stay? | JTBD, adoption friction, switching triggers, and alternatives. |
| Researchers | What data is missing before making a stronger claim? | Missing-data inventory and validation plan. |

Search keywords: AI business model analysis, business model reverse engineering,
business model canvas generator, AI market research, AI competitive analysis,
go-to-market analysis, startup analysis, unit economics analysis, LangGraph
agents, evidence-first research.

## What It Produces

OpenBusiness writes a final Markdown report with this shape:

```markdown
# OpenBusiness Business Model Reverse Engineering Report

**Target:** Notion | **Confidence:** Plausible

## 1. Business Model Canvas

| Key Partners | Key Activities | Value Propositions | Customer Relationships | Customer Segments |
| --- | --- | --- | --- | --- |
| Stripe, AWS, app ecosystem [INFERRED] | Product development, collaboration workflows [VERIFIED:notion.so] | All-in-one workspace [VERIFIED:notion.so] | Self-serve PLG plus enterprise support [INFERRED] | Teams, startups, creators, enterprises [VERIFIED:notion.so] |

## 2. Key Fact Layers

### Verified Facts

- Pricing includes Free, Plus, Business, and Enterprise tiers. [VERIFIED:notion.so/pricing]

### Inferred Assumptions

- Expansion likely depends on team-level workspace adoption. [INFERRED]

### Missing Data

- Actual CAC, gross margin, and cohort retention are not publicly disclosed. [MISSING]

## 3. Assumption Stress Test

## 4. Next Steps
```

Evidence labels are intentionally visible:

| Label | Meaning |
| --- | --- |
| `[VERIFIED:url]` | The claim is supported by a source. |
| `[INFERRED]` | The claim is a reasoned inference from available context. |
| `[MISSING]` | The missing data materially affects confidence. |

## Quick Start

### 1. Clone

```bash
git clone https://github.com/wanikua/OpenBusiness.git
cd OpenBusiness
```

### 2. Install

```bash
./install.sh
```

The installer asks you to choose English or Chinese first, checks Python,
creates a virtual environment if needed, installs the package in editable mode,
and starts the configuration wizard in the selected language. That first
language choice becomes the default terminal UI language and the default report
language for `openbusiness analyze`, unless you explicitly override the report
language later.

If you accept the default `.venv` setup, the installer activates it for the
installation session. In every new terminal, activate it again before running
`openbusiness`:

```bash
source .venv/bin/activate
```

If you declined virtual environment creation, skip this activation step and use
the Python environment where you installed the package.

### 3. Configure Or Reconfigure

```bash
openbusiness config
```

The installer normally starts this wizard automatically. Run it manually when
you skipped the wizard, changed terminals before completing setup, or need to
update keys later.

The setup stores:

| Setting | Required | Notes |
| --- | --- | --- |
| Interface language | Yes | Set by the installer or `openbusiness config --ui-language en`. |
| LLM provider | Yes | `openai`, `anthropic`, or `deepseek` |
| Report language | Yes | Defaults to the interface language; can be changed with `--language`. |
| Provider API key | Yes | OpenAI, Anthropic, or DeepSeek key |
| Tavily API key | No | Enables live search evidence |
| Firecrawl API key | No | Enables page scraping evidence |

Config is saved to `~/.config/openbusiness/config.toml`.

### 4. Run

```bash
source .venv/bin/activate
openbusiness analyze "Notion" --domain notion.so --language en
```

If your shell prompt already shows the virtual environment is active, you do not
need to run `source .venv/bin/activate` again in the same terminal.

The report is written to `output/notion_business_model.md`.

## CLI

```bash
source .venv/bin/activate

openbusiness config
openbusiness config --reset
openbusiness config --language en
openbusiness config --ui-language en
openbusiness show

openbusiness analyze "Notion" --domain notion.so
openbusiness analyze "Costco" --ticker COST
openbusiness analyze "Vercel" --domain vercel.com --output reports/
openbusiness analyze "Notion" --domain notion.so --language en
openbusiness analyze "Notion" --domain notion.so --language zh
openbusiness analyze "Notion" --domain notion.so --ui-language en --language zh
openbusiness analyze "Notion" --domain notion.so --depth deep
```

Analysis options:

| Option | Description |
| --- | --- |
| `--domain`, `-d` | Official company domain for evidence gathering. |
| `--ticker`, `-t` | Public-company ticker for SEC EDGAR lookup. |
| `--output`, `-o` | Output directory. Defaults to `output/`. |
| `--language`, `-l` | Report language for this run. Supports `en` and `zh`. |
| `--ui-language` | Terminal interface language for this run. If `--language` is omitted, the report follows the resolved interface language by default. |
| `--depth` | Research depth. Use `standard` for faster runs or `deep` for broader evidence collection. |

`openbusiness analyze` does not ask for language choices at startup. The
terminal UI language comes from install/config, and the report language follows
that UI language unless you explicitly set `--language`, `OPENBUSINESS_OUTPUT_LANGUAGE`,
or `openbusiness config --language`.

## Environment Variables

Environment variables override local config. They are useful for CI, containers,
and temporary provider switches.

```bash
export OPENBUSINESS_PROVIDER=deepseek
export OPENBUSINESS_UI_LANGUAGE=en
export OPENBUSINESS_OUTPUT_LANGUAGE=en
export DEEPSEEK_API_KEY=sk-xxx
export DEEPSEEK_BASE_URL=https://api.deepseek.com
export DEEPSEEK_TIMEOUT=60
export DEEPSEEK_MAX_RETRIES=1
export DEEPSEEK_MAX_TOKENS=2048
export TAVILY_API_KEY=tvly-xxx
export FIRECRAWL_API_KEY=fc-xxx

openbusiness analyze "Notion" --domain notion.so
```

Interface language precedence:

1. `openbusiness analyze --ui-language en`
2. `OPENBUSINESS_UI_LANGUAGE=en`
3. `ui_language = "en"` in local config
4. Default: `zh`

Report language precedence:

1. `openbusiness analyze --language en`
2. `OPENBUSINESS_OUTPUT_LANGUAGE=en`
3. `output_language = "en"` in local config
4. Resolved interface language

## Bilingual Output

OpenBusiness supports English and Simplified Chinese report generation:

```bash
openbusiness analyze "Notion" --domain notion.so --language en
openbusiness analyze "Notion" --domain notion.so --language zh
openbusiness analyze "Notion" --domain notion.so --ui-language en --language zh
```

Without `--language`, the report follows the terminal UI language selected
during installation or configuration. Use `--language` when you want the UI and
report languages to be different.

The language contract is applied to every analyst node. Final reports also run
a language-purity check:

- English reports warn if generated content contains Chinese characters.
- `zh` reports warn if generated content contains English section headings or
  English-like prose lines.
- Company names, URLs, tickers, metric abbreviations, API/tool names, model
  names, and evidence tags are preserved intentionally.

## Depth Mode

Use `--depth deep` when you want a more serious research pass:

```bash
openbusiness analyze "Notion" --domain notion.so --language zh --depth deep
```

`standard` keeps evidence collection bounded for faster runs. `deep` lets the
evidence collector spend more tool rounds and use broader search depth for
customer proof, hiring signals, ecosystem clues, competitor positioning, and
negative evidence. All analyst nodes still use the same depth standard: major
conclusions must include mechanism, evidence quality, countercase, business
implication, and validation data.

## Pipeline

```text
Company name + optional domain + optional ticker
  |
  v
Evidence Collector
  |-- Tavily search
  |-- Firecrawl scrape
  |-- SEC EDGAR facts
  v
JTBD Analyst
  v
Value Proposition Analyst
  v
GTM Analyst
  v
Unit Economics Analyst
  v
Moat Analyst
  v
Business Model Synthesizer
  v
Assumption Stress Tester
  v
Finalizer
  v
output/<company>_business_model.md
```

Core design principles:

- Evidence first: source material is collected before analysis.
- Claims stay tagged: verified facts, inferred assumptions, and missing data are
  never flattened into one confidence level.
- Tools do deterministic work: unit-economics calculations run in Python, not
  inside model prose.
- The final output is portable Markdown.

## Providers

| Provider | Config key | Notes |
| --- | --- | --- |
| OpenAI | `OPENAI_API_KEY` | Default provider. |
| Anthropic | `ANTHROPIC_API_KEY` | Supported through LangChain Anthropic. |
| DeepSeek | `DEEPSEEK_API_KEY` | Uses an OpenAI-compatible endpoint. |

Optional evidence APIs:

| Service | Config key | Purpose |
| --- | --- | --- |
| Tavily | `TAVILY_API_KEY` | Web search evidence. |
| Firecrawl | `FIRECRAWL_API_KEY` | Website and page scraping. |

If Tavily or Firecrawl is not configured, the pipeline still runs, but more
claims will be marked `[INFERRED]` or `[MISSING]`.

## Project Structure

```text
OpenBusiness/
├── install.sh
├── pyproject.toml
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── llms.txt
├── .env.example
├── docs/
│   ├── PROMOTION.md
│   └── assets/
│       ├── openbusiness-terminal-demo.svg
│       └── openbusiness-report-preview.svg
└── openbusiness/
    ├── cli.py
    ├── language.py
    ├── agents/
    │   ├── analysts/
    │   └── utils/
    ├── graph/
    ├── llm_clients/
    └── tools/
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m ruff check openbusiness
python -m compileall openbusiness
```

## Community

OpenBusiness is meant to be co-built with people who care about better business
research. The goal is not only to ship an AI agent demo, but to build a shared
open-source workflow for evidence-labeled company analysis.

- Star the repository if OpenBusiness helps your research workflow.
- Open an issue for bugs, missing providers, report-quality problems, or
  company-analysis examples that expose weak reasoning.
- Share real analysis examples that show where the pipeline is shallow, slow, or
  missing important evidence.
- Read [CONTRIBUTING.md](CONTRIBUTING.md) before sending a pull request.
- Use [docs/PROMOTION.md](docs/PROMOTION.md) for launch copy, GitHub topic
  suggestions, and community posting templates.
- `llms.txt` is available for AI assistants, answer engines, and developer
  tools that need a compact project summary.

## Troubleshooting

### `./install.sh: Permission denied`

```bash
chmod +x install.sh
./install.sh
```

### `openbusiness: command not found`

Activate the virtual environment used during installation:

```bash
source .venv/bin/activate
```

### The report is mostly inferred

Configure Tavily and Firecrawl so the evidence collector can gather live source
material:

```bash
openbusiness config --reset
```

### The report language is mixed

Run with an explicit language override:

```bash
openbusiness analyze "Notion" --domain notion.so --language en
openbusiness analyze "Notion" --domain notion.so --language zh
```

If the warning persists, retry with a model that follows formatting and
language constraints more strictly.

## License

OpenBusiness is released under the MIT License. See [LICENSE](LICENSE) for the
full license text.
