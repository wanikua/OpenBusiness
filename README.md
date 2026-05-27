# OpenBusiness

> **AI-driven, evidence-first business model reverse engineering.** Give OpenBusiness a company name and it produces a structured business model canvas report with clear fact, inference, and missing-data labels.

OpenBusiness is inspired by [TradingAgents](https://github.com/TauricResearch/TradingAgents), but it intentionally does not copy the bull-vs-bear debate structure. Business analysis should produce a structured decomposition, not a buy/sell vote.

---

## What It Does

```bash
$ openbusiness analyze "Notion" --domain notion.so --language en

  🔍 Evidence Collector         (Tavily + Firecrawl + SEC EDGAR evidence gathering)
  👥 JTBD Analyst               (who pays, who uses it, and what job gets done)
  💎 Value Prop Analyst         (10x-better test)
  🚀 GTM Analyst                (PLG, sales-led, marketplace, community, and more)
  💰 Unit Economics Analyst     (LTV, CAC, break-even math)
  🛡️ Moat Analyst               (five moat types, Porter forces, counter-positioning)
  🧱 Business Model Synthesizer (business model canvas)
  🔬 Assumption Stress Tester   (which assumptions can break the canvas)
  📝 Finalizer                  (final Markdown report)

✅ Report generated: output/notion_business_model.md
```

Every claim is tagged:

- `[VERIFIED:url]` means the claim has a source.
- `[INFERRED]` means the LLM inferred it from context.
- `[MISSING]` means the data is missing and affects confidence.

---

## Install In 5 Minutes

### Step 1: Clone The Repository

```bash
git clone https://github.com/wanikua/OpenBusiness.git
cd OpenBusiness
```

### Step 2: Run The Installer

```bash
./install.sh
```

The installer is interactive and does four things:

1. Checks that Python 3.10 or newer is available.
2. Creates a `.venv/` virtual environment if you approve it.
3. Installs the package with `pip install -e .`.
4. Starts the configuration wizard for API keys and default report language.

### Step 3: Configure API Keys

The wizard asks for:

| Prompt | What To Enter |
| --- | --- |
| `LLM provider [openai/anthropic/deepseek]` | Choose one provider. OpenAI is the default. |
| `Report output language [zh/en]` | Choose `zh` for Simplified Chinese reports or `en` for English reports. |
| `OpenAI API Key (sk-...)` or `Anthropic API Key (sk-ant-...)` | Required. Create one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) or [console.anthropic.com](https://console.anthropic.com/). Input is hidden. |
| `Tavily API Key` | Optional. Adds web search evidence from [tavily.com](https://tavily.com). |
| `Firecrawl API Key` | Optional. Adds page scraping from [firecrawl.dev](https://firecrawl.dev). |

If Tavily or Firecrawl is not configured, the pipeline still runs, but more findings will be marked `[INFERRED]` because less live evidence is available.

Configuration is saved to `~/.config/openbusiness/config.toml` with `0600` permissions.

### Step 4: Run Your First Analysis

```bash
source .venv/bin/activate
openbusiness analyze "Notion" --domain notion.so --language en
```

The report is written to `output/notion_business_model.md`.

---

## CLI Usage

```bash
openbusiness config                         # Run the setup wizard
openbusiness config --reset                 # Re-enter all keys
openbusiness config --language en           # Set the default report language
openbusiness show                           # Show current config without full keys

openbusiness analyze "Notion" --domain notion.so
openbusiness analyze "Costco" --ticker COST
openbusiness analyze "Vercel" --domain vercel.com --output reports/
openbusiness analyze "Notion" --domain notion.so --language en
openbusiness analyze "Notion" --domain notion.so --language zh
```

Analyze options:

- `--domain / -d`: official website domain, used by the evidence collector.
- `--ticker / -t`: US stock ticker, used for SEC EDGAR data when available.
- `--output / -o`: report output directory. Defaults to `output/`.
- `--language / -l`: report output language. Supported values are `zh` and `en`. This overrides config and environment variables for the current run.

---

## Configuration And Environment Variables

Environment variables always override the config file. This is useful for CI, containers, and temporary key or language switches.

```bash
export OPENBUSINESS_PROVIDER=deepseek
export OPENBUSINESS_OUTPUT_LANGUAGE=en
export DEEPSEEK_API_KEY=sk-xxx
export DEEPSEEK_TIMEOUT=60
export DEEPSEEK_MAX_RETRIES=1
export DEEPSEEK_MAX_TOKENS=2048
export TAVILY_API_KEY=tvly-xxx
export FIRECRAWL_API_KEY=fc-xxx

openbusiness analyze "Notion" --domain notion.so
```

Report language precedence:

1. `openbusiness analyze --language en`
2. `OPENBUSINESS_OUTPUT_LANGUAGE=en`
3. `output_language = "en"` in `~/.config/openbusiness/config.toml`
4. Default: `zh`

Language purity:

- `--language en` asks every agent for English-only natural language and warns if the final report contains Chinese characters.
- `--language zh` asks every agent for Simplified Chinese natural language and warns if the final report contains English section headings or English-like prose lines.
- Company names, URLs, ticker symbols, metric abbreviations such as ARPU/LTV/CAC/PLG, tool names, and evidence tags are intentionally preserved.

---

## Architecture

```text
User
  │  company name + optional domain + optional ticker
  ▼
┌─────────────────────────────────────┐
│  Evidence Collector                  │ ← Tavily search + Firecrawl scrape
│                                      │   + SEC EDGAR public filings
└────────┬─────────────────────────────┘
         │  evidence_pack
         ▼
┌─────────────────────────────────────┐
│  JTBD Analyst                        │ ← buyer, user, job, alternatives
└────────┬─────────────────────────────┘
         │  jtbd_report
         ▼
┌─────────────────────────────────────┐
│  Value Prop Analyst                  │ ← 10x-better test
└────────┬─────────────────────────────┘
         │  value_prop_report
         ▼
┌─────────────────────────────────────┐
│  GTM Analyst                         │ ← distribution and acquisition channels
└────────┬─────────────────────────────┘
         │  gtm_report
         ▼
┌─────────────────────────────────────┐
│  Unit Economics Analyst              │ ← LTV/CAC calculation
└────────┬─────────────────────────────┘
         │  unit_econ_report
         ▼
┌─────────────────────────────────────┐
│  Moat & Competition Analyst          │ ← five moat types + Porter forces
└────────┬─────────────────────────────┘
         │  moat_report
         ▼
┌─────────────────────────────────────┐
│  Business Model Synthesizer          │ ← tagged business model canvas
└────────┬─────────────────────────────┘
         │  canvas_report
         ▼
┌─────────────────────────────────────┐
│  Assumption Stress Tester            │ ← fatal assumptions and data gaps
└────────┬─────────────────────────────┘
         │  stress_test_report
         ▼
┌─────────────────────────────────────┐
│  Finalizer                           │ ← final report assembly
└────────┬─────────────────────────────┘
         ▼
 output/<company>_business_model.md
```

Core principles:

- **Linear flow, no debate.** The output is a business decomposition, not a vote.
- **Evidence first.** The pipeline gathers source material before analysis.
- **Tag every claim.** Claims stay labeled as verified, inferred, or missing.
- **Tools are pure math.** Unit economics calculations are Python functions, not LLM arithmetic.
- **Two LLM tiers.** Analyst nodes use a quick model; synthesis and finalization use a deeper model.

---

## Project Structure

```text
OpenBusiness/
├── install.sh
├── pyproject.toml
├── README.md
├── .env.example
├── openbusiness/
│   ├── cli.py
│   ├── agents/
│   │   ├── analysts/
│   │   │   ├── evidence_collector.py
│   │   │   ├── jtbd_analyst.py
│   │   │   ├── value_prop_analyst.py
│   │   │   ├── gtm_analyst.py
│   │   │   ├── unit_econ_analyst.py
│   │   │   ├── moat_analyst.py
│   │   │   ├── synthesizer.py
│   │   │   ├── stress_tester.py
│   │   │   └── finalizer.py
│   │   └── utils/
│   │       └── agent_state.py
│   ├── tools/
│   │   ├── evidence_tools.py
│   │   └── financial_tools.py
│   ├── graph/setup.py
│   ├── language.py
│   └── llm_clients/
│       ├── config.py
│       └── factory.py
└── output/
```

---

## Report Example

```markdown
# OpenBusiness Business Model Reverse Engineering Report

**Target:** Notion | **Confidence:** Plausible

## 1. Business Model Canvas

| Key Partners | Key Activities | Value Propositions | Customer Relationships | Customer Segments |
| --- | --- | --- | --- | --- |
| ... | ... | All-in-one workspace [VERIFIED:notion.so] | PLG self-serve [INFERRED] | ... |

## 2. Key Facts Layer

### Verified Facts

- Pricing includes Free, Plus, Business, and Enterprise tiers. [VERIFIED:notion.so/pricing]

### Inferred Assumptions

- Expansion likely depends on team-level workspace adoption. [INFERRED]

### Missing Data

- Actual CAC and LTV are not publicly available. [MISSING]
```

---

## Troubleshooting

**`./install.sh: Permission denied`**

Run:

```bash
chmod +x install.sh
./install.sh
```

**`python: command not found`**

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/), Homebrew, or your system package manager.

**`openbusiness: command not found`**

If you installed into the virtual environment, activate it first:

```bash
source .venv/bin/activate
```

**Invalid API key or quota errors**

Check the key in your provider dashboard, then run:

```bash
openbusiness config --reset
```

**The report is mostly `[INFERRED]`**

Configure Tavily and Firecrawl so the evidence collector can gather live source material:

```bash
openbusiness config --reset
```

---

## Extending OpenBusiness

To add a new analyst:

1. Create `openbusiness/agents/analysts/your_analyst.py` and export `create_your_analyst(llm)`.
2. Export it from `openbusiness/agents/analysts/__init__.py`.
3. Add the node to `openbusiness/graph/setup.py`.

To add a new tool:

1. Add a `@tool` function under `openbusiness/tools/`.
2. Bind it in the analyst that should use it.
3. Return source-labeled data, or a warning/missing-data value when credentials are not configured.

---

## License

MIT
