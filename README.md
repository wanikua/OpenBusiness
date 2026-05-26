# OpenBusiness

> AI-driven multi-agent business model analysis & reverse engineering.

Drop a company name, get a full **Business Model Canvas** + **Unit Economics** analysis in minutes — powered by a team of AI agents that debate, calculate, and synthesize.

## Architecture

Inspired by [TradingAgents](https://github.com/TauricResearch/TradingAgents), OpenBusiness uses a **LangGraph StateGraph** pipeline with specialized agents:

```
User Input (company name / domain / ticker)
         │
         ▼
┌─────────────────────────────────────────┐
│           Phase 1: Analysis             │
│                                         │
│  📡 Traffic Analyst    💰 Finance Analyst│
│  ⚔️ Competitive Analyst 🎯 Product Analyst│
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│        Phase 2: Bull/Bear Debate        │
│                                         │
│     📈 Optimist  ←→  📉 Pessimist      │
│         (N configurable rounds)         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         Phase 3: Synthesis              │
│                                         │
│  🏛️ Research Director (judge debate)    │
│  📊 Strategy Director (final BMC)       │
└─────────────────────────────────────────┘
                 │
                 ▼
         Markdown Report
```

### Key Design Principles

- **Agents as factory functions** — each `create_xxx(llm)` returns a LangGraph node closure
- **Shared TypedDict state bus** — agents communicate via named fields, never directly
- **Deterministic tools** — financial calculations use pure Python math, not LLM guessing
- **Two LLM tiers** — `quick` for analysts, `deep` for managers (cost optimization)
- **Debate loop** — conditional edges control bull/bear rounds

## Quick Start

```bash
# Clone
git clone https://github.com/wanikua/OpenBusiness.git
cd OpenBusiness

# Install
pip install -e .

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
openbusiness "Notion" --domain notion.so
openbusiness "Costco" --ticker COST
openbusiness "ByteDance" --domain bytedance.com
```

## Project Structure

```
openbusiness/
├── agents/
│   ├── analysts/          # 4 domain analysts
│   │   ├── traffic_analyst.py     # SEO, channels, growth model
│   │   ├── financial_analyst.py   # Revenue, unit economics, P&L
│   │   ├── competitive_analyst.py # Porter's Five Forces
│   │   └── product_analyst.py     # Value proposition, moats
│   ├── researchers/       # Bull/Bear debate
│   │   ├── optimist.py
│   │   └── pessimist.py
│   ├── managers/          # Judges & synthesizers
│   │   ├── research_director.py   # Debate judge
│   │   └── strategy_director.py   # Final BMC generator
│   └── utils/
│       └── agent_state.py         # Shared TypedDict state
├── tools/                 # @tool-decorated deterministic functions
│   ├── financial_tools.py         # LTV/CAC, profitability, revenue analysis
│   ├── traffic_tools.py           # Channel analysis, SEO moat
│   └── web_tools.py               # Company data fetching
├── graph/
│   ├── setup.py                   # LangGraph StateGraph wiring
│   └── conditional_logic.py       # Debate round control
├── llm_clients/
│   └── factory.py                 # OpenAI/Anthropic dual-tier factory
└── cli.py                         # CLI entry point
```

## Output Example

The system generates a comprehensive Markdown report including:

- **Business Model Canvas** (9-grid table)
- **Unit Economics** (LTV, CAC, LTV/CAC ratio, break-even analysis)
- **Moat Analysis** (network effects, switching costs, scale, intangibles)
- **Vulnerabilities** (kill switches, black swan risks)
- **Growth Levers** (actionable insights for builders)
- **Overall Rating** (5-star system across 4 dimensions)

## Extending

Add a new analyst:

1. Create `openbusiness/agents/analysts/your_analyst.py`
2. Follow the factory pattern: `def create_your_analyst(llm) -> (node_fn, tools)`
3. Wire it into `openbusiness/graph/setup.py`

Add a new tool:

1. Create a `@tool`-decorated function in `openbusiness/tools/`
2. Import it in the relevant analyst's module

## License

MIT
