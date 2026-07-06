# Command Reference: !write-brief

Detailed output structure and template for `!write-brief`. Read this file when executing the command. One output type — Growth Summary — with two modes: plain summary and case-building.

---

## General Principles

- **Source:** Pull exclusively from `logs/achievement-log-[year].md`. Do not invent content.
- **Voice:** First-person, past tense, active voice. "I led X." Not "Was responsible for X."
- **Specificity:** Include numbers, outcomes, and scope wherever the log provides them.
- **Tone:** Confident, evidence-grounded, not self-aggrandizing. The work speaks; don't over-editorialize.
- **Audience-agnostic:** Doesn't assume a fixed corporate ladder. A growth summary can go to a manager, a board, or nowhere but the user's own files. Ask who it's for and what the occasion is before drafting if it isn't already known.

---

## Growth Summary

**Purpose:** One template, two modes, sharing the same achievement-log engine, source rules, and voice.

- **Plain summary** (default) — submitted to a manager, a board, or written for yourself. Concise, pasteable into whatever review or reporting system applies with minimal editing.
- **Case-building** — supporting a promotion, a board seat, or a funding/scaling/acquisition case. Comprehensive; structures evidence to build a case rather than list accomplishments.

**Determining mode:** infer from the answer to "who is this for, and what's the occasion?" A promotion, a board-seat case, or a funding/scaling/acquisition case → case-building. A regular check-in, a manager update, or a personal record → plain summary. These are worked examples, not exhaustive — ask when genuinely unclear. `!write-brief growth` and `!write-brief advancement` skip straight to the respective mode without the intake question. In case-building mode, also ask what specifically the user is making the case for (the target position or outcome) — Key Contributions gets organized around that target rather than listed flat.

**Structure:**
```
## [Period] — [Name] Growth Summary
(case-building mode: ## [Current Position] → [Target Position/Outcome])

### Executive Summary  (case-building mode only)

[2–3 sentences: who I am, what I've done this period, why I'm ready for what's next]

### Key Contributions

[Plain summary: 3–5 bullet points, each one achievement from the log. Format:
"[Action verb] [what] → [outcome/impact]. ([timeframe if known])"

Case-building: same achievements, grouped under 2–3 themes relevant to the stated target (e.g. "Systems Leadership," "Cross-Functional Delivery") rather than a flat list — 2–3 achievements per theme, same format.]

### Areas of Growth

[Plain summary: 2–3 sentences on capabilities already developed this period, drawn from log entries.

Case-building: same content, framed as trajectory — what I couldn't do before that I can do now.]

### Areas for Improvement  (plain summary only — omit entirely in case-building mode)

[Forward-facing, constructive recommendations — distinct from Areas of Growth. What would make the next period stronger, drawn from friction points in identity.md and any gaps visible in the log. Omitted in case-building mode: constructive self-criticism undermines a pitch.]

### Readiness Statement  (case-building mode only)

[Final argument paragraph: why now — what the next stage needs that the evidence above already shows I'm doing. Grounded in the log, not generic self-promotion. Distinct from Looking Ahead, which is forward-looking rather than an argument for timing.]

### Looking Ahead

[Plain summary: 1–2 sentences on stated goals for next period, drawn from the two-year self in identity.md.

Case-building: a forward-looking plan for what's next in the target role — distinct from Readiness Statement's "why now" argument.]
```

**Tone guidance:** Plain summary — direct and factual; whoever reads this reads many of them, clarity beats polish. Case-building — an argument, not a summary; structure evidence to build a case, not just list accomplishments.

---

## Cadence Capture

If `preferences.md` has no `brief-cadence` set, ask *"What's your check-in cycle for this — monthly, quarterly, semi-annual, annual, or something else?"* (Monthly is common for founders sending investor updates — worth naming explicitly rather than leaving it to "something else.") Save the cadence and a `next-brief` date. For Cowork users, offer to schedule a reminder a couple weeks out.

**After each run:** offer to update `next-brief` for the next cycle.

---

## Output Format Options

When the user selects their preferred output format:

- **Word document (.docx):** Use the docx skill to generate a formatted file with proper headings and styling. Save to workspace folder.
- **Markdown (.md):** Write directly to the workspace folder as `growth-brief-[date].md`.
- **Google Drive:** Use the Google Drive connector to create the document directly in Drive if connected.
- **Anything else (in chat, a Slack message, etc.):** Deliver directly in the format actually requested rather than forcing one of the three defaults above.

Ask the user which they prefer if they haven't specified. Save their preference to `system/preferences.md` for future use.
