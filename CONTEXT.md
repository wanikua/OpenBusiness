# OpenBusiness Context

## Domain Terms

- **Analysis Run**: one execution of OpenBusiness for a target company. It resolves language, pack, template, pipeline state, report output, and run artifacts.
- **Claim Contract**: the evidence-label rule that every material claim must be `[VERIFIED:url]`, `[INFERRED]`, or `[MISSING]`.
- **Run Artifact**: a reproducible file written for an Analysis Run, including `run.json`, `evidence.json`, `sources.md`, stage reports, and the language-specific report.
- **Stage Catalog**: the ordered list of LangGraph stages, their state keys, labels, and artifact filenames.
- **Profile Registry**: the loader and validator for Analysis Packs and Report Templates.
- **Analysis Pack**: domain-specific guidance that changes evidence and analyst focus.
- **Report Template**: reader-specific guidance that changes report emphasis.
- **Evidence Result**: the structured JSON result returned by evidence tools, including verified source tags, warnings, missing data, or errors.
- **Provider Adapter**: the concrete model-client adapter for an LLM provider at the quick or deep model tier.
