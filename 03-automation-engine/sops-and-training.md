# A.I. STaRR Automation Engine — SOPs & Training

Internal operations doc · Companion to [`README.md`](README.md) and
[`automation-engine.md`](automation-engine.md).
Voice + stack per [`../_shared/brand-guide.md`](../_shared/brand-guide.md).

> **Purpose:** make the engine *runnable by anyone on the team*. This document gives the
> **process maps** (what happens, in order), the **SOPs** (numbered procedures to run each
> workflow), and the **training docs** (onboarding a new operator), plus the
> **hours-saved proof table** that demonstrates the 10+ hr/wk goal.

---

## Part 1 — Process Maps

A process map is the plain step list for each workflow. Use it to understand the flow
before touching a Make scenario. Diagrams for each live in
[`automation-engine.md`](automation-engine.md).

### A · Content Generation
1. Monthly scheduler fires (~25th) for the client.
2. Read pillars + posting cadence from the `Calendar` tab.
3. Loop the target post count; assign date + platform + pillar to each.
4. ChatGPT writes hook + caption + CTA + hashtags per row.
5. Creatomate renders the matching graphic/reel; returns asset URL.
6. Write each row to the `Approval` tab as `Pending`.

### B · Content Approval
1. Drafts land in `Approval` as `Pending`; reviewer gets an email digest.
2. Reviewer opens the tab and reads caption + asset for each row.
3. Reviewer sets status: `Approved`, `Revise` (+note), or `Rejected`.
4. `Revise` rows regenerate through ChatGPT and return to `Pending`.
5. `Approved` rows become eligible for auto-posting.

### C · Auto-Posting
1. Posting-time scheduler fires (e.g. daily 9:00am).
2. Read `Approval`: rows where `status = Approved` AND `date = today`.
3. Router branches by platform (Facebook / Instagram).
4. Publish via Meta Graph API (IG = create container → publish).
5. Update row to `Posted` + permalink; mirror to `Metrics`.
6. On error → error handler emails operator, row left for retry.

### D · Lead Tracking
1. Lead arrives via form webhook or DM/lead event.
2. Append to `Leads` CRM as `New` (name, contact, source, message, time).
3. Send instant branded auto-reply (ChatGPT-personalized if needed).
4. Stamp `first_reply_at`; mirror lead to `Metrics`.
5. Hand off to Follow-Up.

### E · Follow-Up Automation
1. Daily scheduler reads `Leads` (excludes `Won` / `Closed-Lost`).
2. Compute days since `first_reply_at` → pick Day 1 / 3 / 7 step.
3. ChatGPT drafts the step; Email sends it.
4. Update `followup_step`, set `Following`, stamp `last_touch_at`.
5. Stop if replied/`Won`; set `Closed-Lost` after Day 7 with no reply.

### F · Client Reporting Dashboard
1. Weekly scheduler fires (e.g. Monday 8:00am).
2. Pull Meta insights (followers, reach, engagement) for the week's posts.
3. Join with internal counts; write dated snapshot to `Metrics`.
4. Looker Studio refreshes the live dashboard link.
5. ChatGPT writes plain-English wins; Email sends summary + link.

---

## Part 2 — Standard Operating Procedures (SOPs)

Numbered, repeatable procedures. Each lists when to run it, the steps, and how to verify
success. **Status values** used across the engine: `Pending` → `Approved` / `Revise` /
`Rejected` → `Posted` (content); `New` → `Following` → `Won` / `Closed-Lost` (leads).

### SOP-A — Run the Monthly Content Generation Batch
**When:** ~25th of each month, per client. **Owner:** Content Operator.
1. Open the client Google Sheet; confirm the `Calendar` tab pillars + cadence are current.
2. In Make, open the **Content Generation** scenario for that client.
3. Confirm the post count and month variables are correct for next month.
4. Run the scenario (manual run for the first batch; scheduled thereafter).
5. **Verify:** `Approval` tab shows ~30 new `Pending` rows, each with caption + asset URL.
6. If any row is missing an asset, re-run that row (Creatomate render may have timed out —
   see [Troubleshooting](#part-4--troubleshooting)).

### SOP-B — Review & Approve Content
**When:** within 24 hrs of the generation batch (and daily for stragglers). **Owner:** Account Manager.
1. Open the email digest; click through to the `Approval` tab.
2. For each `Pending` row, read the caption against brand voice
   ([brand guide §3](../_shared/brand-guide.md#3-voice--tone)) and preview the asset.
3. Set status: `Approved` (good to go), `Revise` (add a note in the `note` column), or
   `Rejected`.
4. **Verify:** no `Pending` rows remain older than 48 hrs; `Revise` rows have regenerated
   back to `Pending` for a second look.
5. Confirm there are enough `Approved` rows queued to cover the next posting cycle.

### SOP-C — Confirm Daily Auto-Posting
**When:** daily, quick check. **Owner:** Content Operator.
1. After the posting-time run, open the `Approval` tab.
2. **Verify:** today's due rows show `status = Posted` with a permalink + timestamp.
3. Spot-check one permalink to confirm it published correctly on FB/IG.
4. If a row is still `Approved` past its time → check the error handler email and the Meta
   connection (token), then re-run the scenario for that row.

### SOP-D — Handle Inbound Leads
**When:** continuous (automated); human check daily. **Owner:** Account Manager.
1. Open the `Leads` tab; review rows added since last check.
2. **Verify:** each new lead has `status = New`, a `first_reply_at` timestamp, and the
   auto-reply went out.
3. For high-intent leads, jump in personally (set `Won` once booked/closed to stop the
   sequence).
4. Fix any malformed rows (missing contact) and re-trigger the auto-reply if it failed.

### SOP-E — Oversee Follow-Up Sequences
**When:** daily (automated); human check 2–3x/week. **Owner:** Account Manager.
1. Open the `Leads` tab; sort by `status = Following`.
2. **Verify:** follow-up steps are advancing (Day 1 / 3 / 7) and `last_touch_at` updates.
3. Mark `Won` for any lead that replied/converted — this halts the sequence.
4. Confirm Day-7 non-responders flipped to `Closed-Lost` (no infinite chasing).

### SOP-F — Deliver the Weekly Client Report
**When:** weekly (e.g. Monday). **Owner:** Account Manager.
1. After the weekly run, open the `Metrics` tab; confirm a new dated snapshot exists.
2. Open the **Looker Studio dashboard**; confirm numbers refreshed.
3. Read the ChatGPT plain-English summary for accuracy and tone; light-edit if needed.
4. **Verify:** the summary + dashboard link email reached the client and the internal AM.
5. Note any standout win for the next strategy touchpoint.

### SOP-G — Onboard a New Client into the Engine
**When:** at client kickoff. **Owner:** Operations Lead.
1. Clone the **client Sheet template** (tabs: `Calendar`, `Approval`, `Leads`, `Metrics`).
2. Fill `Calendar` with the client's pillars + posting cadence.
3. Duplicate the six Make scenarios; repoint them at the new Sheet.
4. Connect the client's **Meta Graph API** access (Business IG + FB Page; System User
   token — **verify in build**) and **email** sender.
5. Build/clone the client's **Creatomate templates** (brand colors, logo, fonts).
6. Run SOP-A once manually; walk the output through SOP-B as a dry run.
7. Connect **Looker Studio** to the new `Metrics` tab; share the dashboard link.
8. Go live: enable schedulers for A (monthly), C/E/F (recurring), D (always-on webhook).

---

## Part 3 — Training: Onboarding a New Operator

A new team member should be able to run the engine within their first week. This is the
onboarding path.

### Day 1 — Orient
- Read [`README.md`](README.md) and [`automation-engine.md`](automation-engine.md) end to
  end. Understand the one-breath flow: **idea → draft → approval → posted → tracked → reported.**
- Learn the **stack** ([§Integration Stack](automation-engine.md#integration-stack)) and
  the **status values** above. The Google Sheet is the source of truth — *if it's not in
  the Sheet, it didn't happen.*
- Read [`../_shared/brand-guide.md`](../_shared/brand-guide.md) for voice; the operator is
  the human quality gate, so they must know what "on-brand" sounds like.

### Day 2 — Read-only shadow
- Open one live client's Sheet and Make scenarios in **read-only** mode.
- Trace a real post from `Pending` → `Approved` → `Posted` and find its permalink.
- Trace a real lead from `New` → follow-up → `Won`/`Closed-Lost`.
- Open the client dashboard; map each number back to the workflow that produced it.

### Day 3 — Supervised approval (the safest first job)
- Run **SOP-B** on a real batch with the trainer watching.
- Approve/revise/reject 10 rows; discuss each judgment call.
- Practice writing a good `Revise` note (specific, voice-anchored) and watch the
  regeneration.

### Day 4 — Supervised posting + leads
- Run **SOP-C** (confirm daily posting) and **SOP-D** (handle leads) supervised.
- Practice the recovery path: deliberately review an error-handler email and re-run a row.

### Day 5 — Run a full day solo (trainer on call)
- Own the daily checklist below for one client, unsupervised, trainer available.
- Deliver one **SOP-F** weekly report with a self-written summary edit.

### Operator Daily / Weekly Checklist
| Cadence | Task | SOP |
|---|---|---|
| Daily AM | Confirm yesterday/today auto-posts published | [SOP-C](#sop-c--confirm-daily-auto-posting) |
| Daily | Review new leads + auto-replies | [SOP-D](#sop-d--handle-inbound-leads) |
| Daily | Clear `Pending` content older than 24 hrs | [SOP-B](#sop-b--review--approve-content) |
| 2–3x/wk | Check follow-up sequences advancing/stopping | [SOP-E](#sop-e--oversee-follow-up-sequences) |
| Weekly | Run + send client report | [SOP-F](#sop-f--deliver-the-weekly-client-report) |
| Monthly | Generate next month's content batch | [SOP-A](#sop-a--run-the-monthly-content-generation-batch) |
| Per client | Onboard new client | [SOP-G](#sop-g--onboard-a-new-client-into-the-engine) |

### Golden Rules for Operators
1. **The human gate is non-negotiable.** Nothing posts without `Approved`. The engine is
   fast; you keep it safe and on-brand.
2. **The Sheet is truth.** Update status honestly and promptly — every downstream workflow
   reads it.
3. **Stop the chase.** Mark `Won` the moment a lead converts so follow-ups halt.
4. **Watch the error emails.** A silent scenario failure means a client looks inactive —
   re-run and escalate.
5. **Voice first.** When in doubt on a caption, re-read
   [brand guide §3](../_shared/brand-guide.md#3-voice--tone).

---

## Part 4 — Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Row stuck `Approved`, never `Posted` | Meta token expired / API reject | Check error email; refresh Meta token (System User token — **verify in build**); re-run row |
| Content rows missing assets | Creatomate render timeout/credit | Re-run those rows; confirm template field mapping; check render credits |
| Reels not publishing | Reels API limits via third-party | **Verify in build** — may need manual push or workaround |
| Lead logged, no auto-reply | Email module/auth failure | Check email connection; re-trigger auto-reply; verify sender domain deliverability |
| Follow-ups won't stop | Reply not detected / `Won` not set | Manually set `Won`; confirm reply-detection method (**verify in build**) |
| Dashboard numbers stale | Looker connection / weekly run skipped | Re-run Workflow F; reconnect Looker Studio to `Metrics` tab |

---

## Hours-Saved Per Week Summary

Proof of the **10+ hours/week** mandate. "Manual baseline" is the time the same output
takes by hand for **one client**; "After engine" is the residual human time (review +
oversight).

| Workflow | Manual baseline (hrs/wk) | After engine (hrs/wk) | **Saved (hrs/wk)** |
|---|---|---|---|
| A — Content Generation (write + design ~30 posts) | 7.0 | 1.0 | **6.0** |
| B — Content Approval (batch review vs. one-by-one) | 2.5 | 0.5 | **2.0** |
| C — Auto-Posting (schedule + upload daily) | 5.5 | 0.5 | **5.0** |
| D — Lead Tracking (triage, log, first reply) | 4.5 | 0.5 | **4.0** |
| E — Follow-Up Automation (write + send reminders) | 3.5 | 0.5 | **3.0** |
| F — Client Reporting Dashboard (pull + assemble) | 4.5 | 0.5 | **4.0** |
| **Totals** | **27.5** | **3.5** | **24.0** |

**Reduction:** 24.0 saved ÷ 27.5 baseline = **~87% of manual marketing work removed**,
clearing both the **~80% reduction** and **10+ hrs/week** targets — **per client**. Because
scenarios are cloned per client, the savings scale linearly: each additional client adds
~24 hrs/wk of avoided manual work, which is how one operator runs many clients at daily
output.

> **Scaling note:** the residual ~3.5 hrs/wk per client is almost entirely the **human
> approval + oversight** layer — intentional, and the reason the engine stays on-brand and
> safe while running mostly hands-off.

---

## Related Docs
- [`README.md`](README.md) — executive summary + navigation
- [`automation-engine.md`](automation-engine.md) — the build + mermaid diagrams + sources
- [`../_shared/brand-guide.md`](../_shared/brand-guide.md) — voice + standard automation stack
- [`../_shared/pricing-framework.md`](../_shared/pricing-framework.md) — how the engine is packaged
- [`../01-whale-harbor/proposal.md`](../01-whale-harbor/proposal.md) — the engine sold into a client
