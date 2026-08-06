# PROJECT 3 — A.I. STaRR Client Automation Engine

**Internal operating system** · Built by a.i. STaRR · Islamorada, FL
Draws its stack and voice from [`../_shared/brand-guide.md`](../_shared/brand-guide.md#5-standard-ai-automation-stack).

> This is **not** a client pitch. It is the internal engine a.i. STaRR runs to
> produce, approve, publish, track, and report on client marketing — so one
> operator can do the work of a full marketing team.

---

## Executive Summary

a.i. STaRR sells "marketing that runs itself." The Client Automation Engine is the
machine that makes that promise true on the inside. It chains six Make.com workflows
across one shared stack so client content moves from **idea → draft → approval →
published → tracked → reported** with minimal human touch.

**The mandate:**

| Goal | Target |
|---|---|
| Reduce manual marketing work | **~80%** |
| Time saved per operator, per week | **10+ hours** (engine total: **~24 hrs/wk** — see [SOPs](sops-and-training.md#hours-saved-per-week-summary)) |
| Output | Daily posting per client, on schedule, without an operator at the keyboard |
| Scalability | Add a client by adding a row, not a hire |

**How it works in one breath:** A schedule trigger fires → ChatGPT drafts captions and
Creatomate renders graphics/reels → drafts land in Google Sheets for one-tap human
approval → approved rows auto-publish to Facebook and Instagram via the Meta Graph API
→ inbound leads are logged and auto-replied → unconverted leads get a timed follow-up
sequence → every metric rolls up into a live client dashboard.

**The six workflows:**

1. **Content Generation** — ChatGPT + Creatomate draft a month of posts from each
   client's pillars.
2. **Content Approval** — a Google Sheet status column gates everything; nothing
   publishes without a human "Approved."
3. **Auto-Posting** — approved rows publish to FB + IG on schedule via Meta Graph API.
4. **Lead Tracking** — form/DM inquiries log to a CRM sheet with instant auto-reply.
5. **Follow-Up Automation** — timed email sequence chases unconverted leads.
6. **Client Reporting Dashboard** — metrics auto-refresh into one shareable link.

The full build, tool-by-tool wiring, and **mermaid automation diagrams** live in
[`automation-engine.md`](automation-engine.md). The process maps, SOPs, training docs,
and the hours-saved proof table live in [`sops-and-training.md`](sops-and-training.md).

---

## Navigation

| File | What's inside |
|---|---|
| [`README.md`](README.md) | This page — executive summary + navigation |
| [`automation-engine.md`](automation-engine.md) | The build: six workflows (trigger → steps → tools → output → hours saved), integration stack, and mermaid diagrams |
| [`sops-and-training.md`](sops-and-training.md) | Process maps, numbered SOPs, team-onboarding training docs, hours-saved summary table |

**Shared references:**
- [Brand & Positioning Guide](../_shared/brand-guide.md) — voice + the standard AI automation stack
- [Pricing Framework](../_shared/pricing-framework.md) — how the engine is packaged into retainers
- [Deliverable Template](../_shared/deliverable-template.md) — 13-section client proposal standard
- [Whale Harbor proposal](../01-whale-harbor/proposal.md) — example of the engine sold into a client (see its AI Automation section)

---

## The Stack at a Glance

See [`automation-engine.md` → Integration Stack](automation-engine.md#integration-stack)
for the full wiring. In short:

| Tool | Role in the engine |
|---|---|
| **Make.com** | Orchestration — runs all six scenarios |
| **Google Sheets** | Source of truth — calendars, approval queue, lead CRM, metrics |
| **ChatGPT (OpenAI)** | Caption + content generation |
| **Creatomate** | Automated graphic + reel rendering from templates |
| **Facebook + Instagram (Meta Graph API)** | Auto-publishing |
| **Email** | Auto-reply, follow-up sequences, approval + report delivery |

> Items marked **verify in build** are platform behaviors (API limits, token lifetimes,
> Reels publishing support) that must be confirmed in a live Make scenario before a
> client goes live. They are flagged inline throughout
> [`automation-engine.md`](automation-engine.md).
