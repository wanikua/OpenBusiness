# Extending OpenBusiness

OpenBusiness is designed to grow through small, reviewable extensions that make
reports more accurate, more domain-aware, or easier to verify.

The most useful extension types are:

- analysis packs
- report templates
- evidence tools
- improved analyst prompts

## Evidence Label Contract

Every extension must preserve the core evidence labels:

| Label | Meaning |
| --- | --- |
| `[VERIFIED:url]` | Directly supported by a cited source. |
| `[INFERRED]` | Reasoned from available evidence without direct source support. |
| `[MISSING]` | Important data is unavailable, private, absent, or not collected. |

Do not write extensions that hide uncertainty. A strong OpenBusiness report is
useful because it distinguishes facts from assumptions and gaps.

## Analysis Packs

Built-in packs live in:

```text
openbusiness/resources/packs/
```

Each pack is a TOML file:

```toml
id = "example-pack"
name = "Example Pack"
description = "When to use this pack."

evidence_focus = [
  "What the evidence collector should prioritize.",
  "Which sources are especially important.",
]

analyst_focus = [
  "What analysts should pay attention to.",
  "Which assumptions need extra skepticism.",
]
```

Run a built-in pack:

```bash
openbusiness analyze "Vercel" --domain vercel.com --pack saas
```

Run a local custom pack:

```bash
openbusiness analyze "Example" --domain example.com --pack-file ./my-pack.toml
```

Good packs are narrow enough to improve reasoning, but not so narrow that they
overfit one company.

## Report Templates

Built-in templates live in:

```text
openbusiness/resources/templates/
```

Each template is a Markdown file with TOML front matter:

```markdown
+++
id = "example-template"
name = "Example Template"
description = "Who this report lens is for."
+++

Emphasize:

- what the reader needs to decide
- what evidence should receive more attention
- what shallow conclusions to avoid
```

Run a built-in template:

```bash
openbusiness analyze "Vercel" --domain vercel.com --template investor-memo
```

Run a local custom template:

```bash
openbusiness analyze "Example" --domain example.com --template-file ./my-template.md
```

Templates change the reader lens. They should not invent sections that require
data the pipeline cannot collect, and they must keep evidence labels visible.

## Evidence Tools

Evidence tools live in:

```text
openbusiness/tools/
```

Good evidence tools:

- return source URLs or explicit missing-data messages
- fail gracefully when API keys are missing
- avoid pretending scraped or searched data is complete
- keep deterministic work in code instead of model prose

## Checks

Before opening a pull request:

```bash
python -m ruff check openbusiness
python -m compileall openbusiness
bash -n install.sh
python -m openbusiness.cli packs
python -m openbusiness.cli templates
```
