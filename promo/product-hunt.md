# Product Hunt Launch Package — OpenBusiness

## Tagline (≤60 chars)

`Notion's LTV/CAC was 1.6x. Stress-test the model.`

(55 chars)

**Alternates:**
- `Find the assumption that breaks the business model.` (51)
- `Business model reports with verified/inferred/missing tags.` (59)

## Description (≤260 chars)

> Notion modeled at 1.6x LTV/CAC; 6% churn pushed it to 1.07x, while 2% churn reached 3.2x. OpenBusiness turns public evidence into a first-pass business model report, tags claims 🟢/🟡/🔴, and stress-tests assumptions.

(235 chars)

---

## First comment (maker intro)

> Maker here 👋
>
> I built OpenBusiness because I kept seeing business model reports where the cleanest-looking number was usually the least trustworthy one.
>
> The example that made the tool feel useful was Notion. The report modeled LTV/CAC at 1.6x, below the healthy 3x benchmark. Then the stress tester showed the fragile part: if monthly churn is 6% instead of the inferred 4%, LTV/CAC falls to 1.07x. If churn is 2%, it reaches 3.2x.
>
> That is what I wanted from the tool: not just "here is a canvas," but "here is the assumption that changes the conclusion."
>
> OpenBusiness is a 9-agent CLI that gathers public evidence, builds a business model canvas, runs unit economics in Python, and tags claims as 🟢 verified, 🟡 inferred, or 🔴 missing. It supports OpenAI, Anthropic, and DeepSeek.
>
> Free, MIT, sample reports for Notion / Vercel / OpenAI in the repo. I would especially value feedback on where the report still over-infers from thin evidence.

---

## Gallery shot list (5 shots, in order)

| # | Asset | Caption |
|---|---|---|
| 1 | `docs/assets/openbusiness-report-preview.svg` (rendered as PNG, 1600×900) | **The output.** Each metric in the report carries a tag, so readers can separate sourced numbers from inferred ones. |
| 2 | Screenshot of the Notion report's "Assumption Stress Test" section | **The stress tester is the punchline.** It tells you which assumption, if wrong, changes the analysis. |
| 3 | `docs/assets/openbusiness-terminal-demo.svg` (rendered as PNG, 1600×900) | **9-agent linear pipeline.** Evidence first, then JTBD, value prop, GTM, unit economics, moat, canvas, stress test, final. |
| 4 | Architecture diagram (the ASCII block in README rendered cleanly) | **No debate, no voting.** Business analysis is a decomposition, not a buy/sell choice. |
| 5 | Install command on a clean terminal background | **One command.** `pipx install openbusiness` → `openbusiness analyze "Notion"`. |

> Generate shots 2, 4, 5 with any terminal-screenshot tool (e.g., `silicon`, `freeze`, or Carbon). Shots 1 and 3 already exist as SVG — convert with `rsvg-convert docs/assets/openbusiness-report-preview.svg -o demo-report.png -w 1600`.

---

## Hunter outreach DM

> Hey — launching an open-source CLI on Product Hunt next [day]: **OpenBusiness**.
>
> The Notion sample modeled LTV/CAC at 1.6x, then showed how one churn assumption could push it to 1.07x or 3.2x. The product turns public evidence into a first-pass business model report and tags claims 🟢 verified / 🟡 inferred / 🔴 missing.
>
> It is built for founders, strategists, and investors who want a structured report without made-up ARPU or churn numbers. MIT, samples for Notion + Vercel + OpenAI in the repo.
>
> Would you be open to hunting it? Repo: https://github.com/wanikua/OpenBusiness — happy to send the assets and draft post.

---

## Launch checklist

- [ ] Schedule for Tuesday/Wednesday 00:01 PT (best PH timing)
- [ ] Topic tags: `Artificial Intelligence`, `Developer Tools`, `Open Source`, `Productivity`
- [ ] Pin first comment within 30 seconds of launch
- [ ] Reply to every comment within 2 hours of launch day
- [ ] Cross-post the X thread (`promo/twitter-thread.md`) at 09:00 PT same day with PH link
- [ ] Share in: maker communities (Indie Hackers, Hacker News if not already), relevant Discord/Slack
- [ ] Update README PyPI badge after launch reaches >50 upvotes
