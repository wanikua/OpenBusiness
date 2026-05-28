# Product Hunt Launch Package — OpenBusiness

## Tagline (≤60 chars)

`Reverse-engineer any company's business model. Honestly.`

(57 chars)

**Alternates:**
- `AI business model teardowns — with every claim tagged.` (54)
- `Business model X-ray. Verified vs. inferred vs. missing.` (56)

## Description (≤260 chars)

> Drop in a company name. Get a full business model canvas where every claim is tagged 🟢 verified / 🟡 inferred / 🔴 missing — plus a stress test of which assumptions, if wrong, would invalidate the analysis. Open source, MIT, bring your own LLM key.

(252 chars)

---

## First comment (maker intro)

> Maker here 👋
>
> I got tired of "AI business analysis" tools that fabricate confident-sounding ARPU, churn, and LTV numbers for private companies. So I built one that's structurally forced to tag every claim — 🟢 verified, 🟡 inferred, or 🔴 missing — and includes a stress tester that tells you which assumption, if wrong, breaks the entire analysis.
>
> Ran it on Notion. Told me LTV/CAC = 1.6x, then explained: *"4% monthly churn is the load-bearing assumption. If actual churn is 6%, LTV/CAC → 1.07x. Unsustainable."* That's the kind of output I wanted to read myself.
>
> 9-agent linear pipeline (no bull/bear debate — business analysis isn't a vote). Unit economics done in Python, not LLM. Two-tier model routing keeps full reports at $0.10–$0.40 each.
>
> Free, MIT, sample reports for Notion / Vercel / OpenAI in the repo. Would love feedback — especially: which agent's prompt would you rewrite first?

---

## Gallery shot list (5 shots, in order)

| # | Asset | Caption |
|---|---|---|
| 1 | `assets/demo-report.svg` (rendered as PNG, 1600×900) | **The output.** Every metric in the report carries a tag. You can see at a glance which numbers are real and which are guesses. |
| 2 | Screenshot of the Notion report's "Assumption Stress Test" section | **The stress tester is the punchline.** It tells you which assumption, if wrong, kills the analysis. |
| 3 | `assets/demo-terminal.svg` (rendered as PNG, 1600×900) | **9-agent linear pipeline.** Evidence first, then JTBD, value prop, GTM, unit economics, moat, canvas, stress test, final. |
| 4 | Architecture diagram (the ASCII block in README rendered cleanly) | **No debate, no voting.** Business analysis is a decomposition, not a buy/sell choice. |
| 5 | Install command on a clean terminal background | **One command.** `pipx install openbusiness` → `openbusiness analyze "Notion"`. |

> Generate shots 2, 4, 5 with any terminal-screenshot tool (e.g., `silicon`, `freeze`, or Carbon). Shots 1 and 3 already exist as SVG — convert with `rsvg-convert assets/demo-report.svg -o demo-report.png -w 1600`.

---

## Hunter outreach DM

> Hey — launching an open-source CLI on Product Hunt next [day]: **OpenBusiness**. It reverse-engineers a company's business model and tags every claim 🟢 verified / 🟡 inferred / 🔴 missing (so no fabricated ARPUs).
>
> It's an honest take on "AI business analysis" — built for founders / strategists / investors who want a structured teardown without the LLM hallucination tax. MIT, samples for Notion + Vercel + OpenAI in the repo.
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
