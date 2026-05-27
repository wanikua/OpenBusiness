# Contributing to OpenBusiness

Thanks for helping improve OpenBusiness. This is a co-building project for
people who want better evidence-first company analysis. Contributions should
make reports more accurate, more useful, easier to verify, easier to extend, or
easier to run.

## Co-Building Principles

- Evidence beats confident prose.
- Clear missing data is better than fake certainty.
- Preserve the evidence labels. Knowing, inferring, and admitting missing data
  are separate states.
- Practical workflows matter as much as model output quality.
- Bilingual support should be treated as a first-class feature.
- Good examples are valuable contributions, even when they reveal weaknesses.

## Good First Contributions

- Improve analyst prompts with clearer reasoning standards.
- Add evidence sources or make existing tools more reliable.
- Add an analysis pack for a specific domain.
- Add a report template for a specific reader workflow.
- Add provider support for more LLM APIs.
- Improve bilingual output quality.
- Add report examples that expose weak reasoning or missing data.
- Improve installation, documentation, or troubleshooting.
- Share benchmark companies where the current pipeline produces shallow,
  generic, or wrong conclusions.

## Local Setup

```bash
git clone https://github.com/wanikua/OpenBusiness.git
cd OpenBusiness
./install.sh
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Checks

Run these before opening a pull request:

```bash
python -m ruff check openbusiness
python -m compileall openbusiness
python -m openbusiness.cli packs
python -m openbusiness.cli templates
```

If your change affects installation, also run:

```bash
bash -n install.sh
```

## Pull Request Guidelines

- Keep changes focused. Avoid mixing unrelated refactors with feature work.
- Preserve evidence labels: `[VERIFIED:url]`, `[INFERRED]`, and `[MISSING]`.
- Analysis packs and report templates may change the lens, but must not weaken
  the evidence-label contract.
- Do not commit API keys, generated reports, local config, or virtual
  environments.
- Keep README and top-level project metadata in English.
- When changing prompts, explain how the change improves report depth, evidence
  quality, language purity, or runtime.
- When changing tools, make failure modes explicit and graceful.

## Issue Guidelines

Useful issues include:

- A company analysis that produced shallow or wrong reasoning.
- A missing data source that would materially improve evidence quality.
- A proposed analysis pack or report template with a concrete company example.
- A provider or model that fails to follow tool calls or language constraints.
- Installation friction on a specific OS, shell, or Python version.

Please include the command you ran, expected behavior, actual behavior, and any
safe-to-share logs. Do not paste private API keys.

## Community Standards

Keep discussions technical and evidence-oriented. Strong disagreement is fine;
unsupported claims, personal attacks, and promotional spam are not.
