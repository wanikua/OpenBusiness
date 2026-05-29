# Sample Report

A real, unedited report produced by OpenBusiness from public evidence. Every
claim is tagged `[VERIFIED:url]`, `[INFERRED]`, or `[MISSING]` — this sample
shows exactly what the tool outputs, including the assumption stress test.

| Company | Language | File | Pack |
| --- | --- | --- | --- |
| Notion | English | [notion-business-model.en.md](notion-business-model.en.md) | general |

This is the example referenced in the project's launch posts: the tool modeled
LTV/CAC at **1.6x** (below the healthy 3x benchmark), then the stress tester
showed the churn assumption is what flips the conclusion — 6% monthly churn
drops it to 1.07x, 2% lifts it to 3.2x. All of those figures are labeled
`[INFERRED]` or `[VERIFIED:calculation]` in the report, not presented as sourced
Notion financials.

Reproduce it:

```bash
openbusiness analyze "Notion" --domain notion.so --language en
```
