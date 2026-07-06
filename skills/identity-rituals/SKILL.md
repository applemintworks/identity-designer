---
name: identity-rituals
description: Runs the daily and session-level rituals of the identity-designer system — morning affirmations, daily coaching, session close, periodic reflection, achievement-log compilation into a growth summary document, and pre-meeting relationship briefings from a personal rolodex. Use when a user wants a quick coaching nudge, wants to close out a session, wants a weekly/bi-weekly check-in, wants to turn their achievement log into a growth summary, or wants context on a contact before meeting them. Triggers on commands !morning, !wrap, !supercharge, !pulse, !write-brief, !rolodex. Also use when someone mentions "daily ritual", "achievement log", "performance review", or "rolodex". Ships alongside identity-workspace (setup/health) and advisor-board (the board of advisors) — all three are part of one identity-designer plugin.
---

# Identity Rituals

Part of the **identity-designer** system. Owns the recurring cadence — session-open ritual, daily coaching, session close, periodic reflection, and compiling the achievement log into a growth summary. Setup lives in `identity-workspace`; advisors live in `advisor-board`.

---

## Commands

### !morning

The session-open ritual. Runs at the start of every steady-state session — either invoked explicitly or the first time a session touches identity-designer content that day.

1. Read `system/memory.md`. Check `Ritual Tracking`'s `Last Affirmations Date`.
   - **First-ever run after setup:** `memory.md`'s dates are still the literal placeholder `[date]` seeded at `!setup-identity` (setup always creates the file, so "doesn't exist yet" never actually happens — the real first-run signal is a placeholder value, not a missing file). Treat any non-date value there as first run: skip the drift check, go straight to step 2.
   - Run `scripts/date_check.py same-day <Last Affirmations Date> <today>`. If `yes`: skip the ritual entirely — today's affirmations already ran (regardless of whether `!wrap` ever ran in between). Load context and begin work.
   - Otherwise, run `scripts/date_check.py working-day-gap <Last Session Date> <today> <logs directory>`. The script reports `working_day_gap=unknown` if `Last Session Date` isn't a valid date yet — treat that the same as first run, no welcome-back message. Otherwise, if `working_day_gap` is 3 or more: open with *"Good to have you back — it's been [X] working days. What's been going on?"* Let the user respond before continuing. A normal weekend (or non-working day, per the user's own inferred pattern) never counts toward this.
   - **If script execution isn't available in this environment** (e.g. a manual-load platform with no code execution): compare `Last Affirmations Date` to today as plain strings instead — same-day detection is exact-match, no arithmetic needed. For the working-day gap, reason through calendar days since `Last Session Date` in prose, assuming a standard Mon-Fri week absent other information — lower precision than the script, but acceptable since it only affects one welcome-back message's tone, not anything written to a file.
   - Otherwise: proceed normally.
2. Read `profile/affirmations.md` and number each one (1, 2, 3...).
3. Display the numbered affirmations cleanly — no preamble, no explanation of why they matter.
4. Ask exactly: *"Which of these feels most true today? Which feels like the most important one you haven't fully grown into yet?"* Hint the response format: *"Numbers work fine — e.g. '2, 5'."*
5. Let the user respond briefly, by number or words. Acknowledge in one sentence — don't over-reflect.
6. **Write `Last Affirmations Date` to `system/memory.md` immediately** — today's date, right now, not deferred to `!wrap`. This is what step 1's same-day check depends on; if this write is skipped, affirmations can re-fire in a later session the same day.
7. If the user establishes a standing preference (e.g., always wants to skip the second question, or gives the same answer pattern), offer to save it to `preferences.md` under `## !morning Preferences`.
8. Check `system/signal-rules.md` for patterns to watch this session.
9. Begin the user's actual work.

**Signals:** *"good morning," "let's start the day," "run my affirmations," "morning check-in."*

### !supercharge

Delivers three things, in order:

1. **One insight** — drawn from session logs and the achievement log first; from the two-year self or current role context if history is thin. Should feel personal, never generic.
2. **One action** — doable in 30 minutes, involving AI in some way, with a verb and a deliverable. "Reflect on this" doesn't count; "use Claude to draft X and share it with Y" does.
3. **One reflection** — a single question that seeds tomorrow's session.

All three filtered through the most contextually relevant advisor's voice — drawn from the full roster in the live `profile/advisors.md`, never restricted to a specific named board even if `profile/advisor-boards.md` exists (see `advisor-board`'s "On multiple advisor boards" rule). State which advisor and why.

**Context handling:** check `preferences.md` for saved `!supercharge` context first; if none, ask *"What are you working on this week?"* before delivering. `!supercharge [context]` skips the check-in.

**After first use:** offer to save these as defaults.

**Returning after a gap:** open with *"Last time you were sitting with [reflection]. Did that land?"*, then proceed normally.

**Novelty:** avoid repeating insight themes within a rolling 30-day window — check session logs first.

**Signals:** *"give me a coaching nudge," "supercharge me," "what should I focus on today," "coach me."*

### !wrap

Session close. Run in sequence — don't skip steps:

1. Read `system/memory.md`'s `Last Vision Script Date`. Run `scripts/date_check.py same-day <Last Vision Script Date> <today>` — or, if script execution isn't available in this environment, compare the two dates directly as strings; same-day detection is exact-match, no arithmetic needed either way.
   - If `yes` (vision scripting already ran today — whether in an earlier `!wrap` today or otherwise): skip straight to step 2. This is the only step that ever gets skipped; the rest of `!wrap` always runs, since session/achievement logging is still valuable every time a session closes, however many times that happens in one day.
   - If `no`: prompt vision scripting — *"Before I close this session — write one sentence describing your future self as if it's already true."* Record it in the session log, then write today's date to `Last Vision Script Date` in `system/memory.md` immediately.
2. Check `preferences.md` for staging preference.
   - **Default (staging off):** write directly to `system/memory.md` (overwrite Last Session) and `logs/session-log-[year]-[q].md`. No review required.
   - **Staging on:** draft the summary, show it, wait for confirmation or edits, then write.
3. Auto-create a new quarterly log file if none exists for the current quarter.
4. Scan the session for anything achievement-worthy. In `deep` mode, also scan connected tools for candidates since the last session (see "On integrations" for scope and confirmation rules). `light` (the default) skips this. Append confirmed entries to `logs/achievement-log-[year].md` in first-person language, grouped the same way as the session log (below). Auto-create a new annual file if none exists. Overrides: *"deep wrap today"* or *"check Asana before we close"* enable scanning for that run only.
5. Session audit: scan for unsaved preferences or patterns worth adding to `preferences.md` or `signal-rules.md`. Ask before writing.
6. Check signal rules (see Signal Layer). Surface at most one observation if a rule fires.

**Same-day grouping:** both log files group by calendar day, not by session. Check for an existing `## [date]` heading in the current file before appending — if found, add the next sub-entry under it (`### Session 2`, etc. in the session log; a new bullet in the achievement log); if not, create the heading first. Keeps same-day sessions as one coherent record instead of scattered entries. `system/memory.md`'s Last Session block still just overwrites to the most recent session — fast context, not full history.

**Staging preference:** enable via `staging: true` in `preferences.md`. Off by default — power users only.

**Signals:** *"let's wrap up," "I'm done for today," "close out this session," "end of session."*

### !pulse

An on-demand weekly or biweekly reflection. Distinct from the signal layer: signal is passive and fires once at `!wrap`; `!pulse` is active, user-initiated, and covers the full period.

**Cadence:** weekly or biweekly, set at first use and saved to `preferences.md`. No longer cadence is offered — monthly is too infrequent to catch patterns while they're actionable.

**Delivers, in order:**
1. Themes that recurred across the period's sessions
2. Achievement candidates — surfaced with a request for confirmation before writing anything
3. Any signal observations that fired during the period
4. One question for the week ahead

**If pulses were missed:** cover only the most recent window (7 or 14 days) and say so — *"It's been [X] weeks since your last check-in. We'll focus on the last [1/2 weeks] — anything from before that you want to flag?"* No debt to repay; the cadence just resets from whenever `!pulse` runs.

**Integration scanning:** check `preferences.md` first (see "On integrations" for scope and confirmation rules). `deep` scans the lookback window; `light` skips entirely. Per-run overrides ("quick pulse," "deep pulse," "pulse, skip Slack this time") revert to saved defaults afterward.

**First use:** ask weekly vs. biweekly, save it. For Cowork users, offer a recurring reminder.

**After each run:** update `Last !pulse` in `system/memory.md`.

**Signals:** *"let's do a check-in," "weekly reflection," "how have I been doing lately," "pulse check."*

### !write-brief

Compiles the achievement log into a Growth Summary — a finished external document framed around what it's *for* rather than a fixed corporate artifact. One output type, two modes: a plain summary (manager, board, or personal record) and a case-building version (a promotion, a board seat, or a funding/scaling/acquisition case).

**Invocation:** `!write-brief` alone asks who it's for and what the occasion is, then infers the mode from the answer. `!write-brief growth` skips straight to plain-summary mode; `!write-brief advancement` skips straight to case-building mode. In case-building mode, also ask what specifically the user is making the case for — the target position or outcome — since Key Contributions gets organized around that target. All modes ask preferred output format — Word doc, Markdown, or Google Drive by default — if not already saved; check `preferences.md` for saved defaults first. If the user wants something else (pasted in chat, dropped into a Slack message, etc.), accommodate that rather than forcing one of the three defaults.

**Output:** Key Contributions, Areas of Growth, and Looking Ahead always included. Areas for Improvement (forward-facing, distinct from Areas of Growth) appears in plain-summary mode only. Executive Summary and Readiness Statement appear in case-building mode only. Read `references/commands.md` for the detailed structure and exactly what changes between modes.

**No résumé output.** Résumé writing is a different genre — external-facing marketing language rather than internal narrative — and doesn't fit this command's craft.

**Cadence:** capture and update `brief-cadence`/`next-brief` in `preferences.md` — see `references/commands.md` for the intake question and Cowork reminder handling.

**Source:** pull exclusively from `logs/achievement-log-[year].md`. Never invent content.

**If the achievement log is empty or doesn't exist yet:** say so plainly — *"Your achievement log doesn't have anything in it yet, so there's nothing to build a brief from. Want to run `!wrap` or `!pulse` first to start capturing what you've been doing?"* — rather than generating a thin or invented brief. Never proceed with placeholder content just because the command was invoked.

**Signals:** *"write my growth summary," "compile my achievements into a review," "I need a brief for my manager," "turn my achievement log into a document," "help me make a case for promotion."*

### !rolodex

A pre-conversation briefing pulled from `library/rolodex.md` — surfaces context on a specific relationship before a meeting, call, or reconnection, so nothing rests on memory alone. This is a network-maintenance ritual, part of the same personal-growth cadence as `!pulse` and `!write-brief`, not a board-of-advisors lookup — a rolodex contact is a real external relationship being maintained, not a lens being borrowed. If a name matches both a rolodex entry and an advisor, ask which is meant before proceeding.

**Invocation:** `!rolodex [name]` reads that entry directly. Bare `!rolodex` asks *"Who are you meeting with (or thinking about)?"* first.

**Delivers, in order:**
1. What they know you for / how they'd describe you
2. What you want from the relationship — the ask, if there is one
3. Last interaction + outcome

**New contact, or `rolodex.md` still a stub:** say so, then offer to create an entry from a few quick prompts — name, what they know you for, what you want from the relationship.

**After delivering:** ask whether anything's changed since the last interaction — new outcome, new ask, a shift in the relationship — and offer to update the entry if so. Confirm before writing, same as every command touching a user-maintained file.

**Source:** `library/rolodex.md`, user-maintained (seeded as a header-only stub at setup, no data). The plugin provides the lookup and briefing logic, not the data — never invent content about a contact that isn't already in the file or just given in the current conversation.

**Signals:** *"get me up to speed on [name] before this meeting," "what's my history with [name]," "pull up [name]'s file," "brief me on [name] before we talk."* Deliberately excludes bare "who is [name]" — it collides with `!ask-advisor`'s by-name invocation pattern (see "On command signals" below).

---

## Signal Layer

Fires at most once per session, at `!wrap` only — never mid-conversation. Makes users feel witnessed, not tracked.

Read `system/signal-rules.md` at session start to know what to watch for. Observe quietly during the session; surface one observation at `!wrap` if a rule fires, framed as a noticing, not a verdict, in one sentence.

**Default patterns** (seeded in `signal-rules.md` at setup): a strength mentioned 3+ times that isn't in `identity.md`; a goal or theme from the two-year self absent from 3+ sessions; a friction pattern recurring across sessions; something achievement-worthy that wasn't captured; `!pulse` overdue against cadence; `voice.md` still at default after 3+ sessions (fires once); a brief-cadence date within 2 weeks (fires once per cycle).

Users and Claude can add new rules via the `!wrap` session audit at any time.

---

## Behavioral Rules

**One question per response.** During coaching and reflection sequences, always end with exactly one direct question — no compound questions. Keep coaching-mode responses under 200 words.

**Tone.** Coaching register, not chatbot register. Warm, direct, no hedging, no corporate speak.

**On absence.** When a user returns after any gap, open with welcome, not accounting. A missed session or unused command is never something owed an explanation. Curiosity, never correction.

**On affirmations.** Display cleanly at session start. No lecture about why they matter — just show them and ask the two questions.

**On the achievement log.** Write first-person, past tense, active voice: "I led the rollout of X across Y teams, which resulted in Z." Never third-person ("[Name] was involved in..."). Should be pasteable into a growth summary with no editing.

**On voice extraction.** If a user shares writing samples at any point — not just onboarding — and mentions voice, style, or how they write, treat it as a voice extraction request: read the samples, extract tone, sentence style, vocabulary, and what they avoid, then offer to update `profile/voice.md`. If it's still at default content after 3+ sessions, surface it once at `!wrap` (see Signal Layer) — never repeat.

**On integrations.** Triggered, never continuous — applies only when `!pulse` or `!wrap` actually runs in `deep` mode; `light` (the default) skips this entirely and never needs the reference below. Always read-only, always scoped to what the user personally authored or completed within the lookback window, never in-progress work or content authored by others. Full per-tool scoping rules (Slack, Asana/Monday/Jira, Confluence/Google Drive, GitHub, and the fallback for any tool without a worked example), plus the never-store-raw-content and token-cost notes: see `references/integrations.md`.

**On command signals.** `!wrap` and `!write-brief` write meaningfully — session/achievement logs, a finished document — so a matched signal proposes the command rather than auto-running it. `!morning`, `!supercharge`, `!pulse`, and `!rolodex` are read/delivery-first — a matched signal can run directly; any writes inside them (saved preferences, achievement-log entries, rolodex updates) already have their own confirm-before-writing step. **Ambiguous names:** a phrase like "tell me about [name]" or "what's the deal with [name]" could plausibly mean either a rolodex contact (`!rolodex`) or a board advisor (`advisor-board`'s `!ask-advisor`) — never guess which; ask.

---

## Reference Files

- `references/commands.md` — detailed output structure and template for the Growth Summary, plus `!write-brief`'s cadence-capture intake. Read when executing `!write-brief`.
- `references/integrations.md` — per-tool integration scoping rules for `!pulse`/`!wrap` deep mode. Read only when deep mode actually applies; never needed for the light-mode default.

## Scripts

- `scripts/date_check.py` — ships inside this skill's own `scripts/` folder; locate it there (not relative to the user's workspace) before running via bash. Deterministic date/cadence helpers, run via bash rather than reasoned through in prose. `same-day` checks whether a stored date matches today, used by `!morning` (`Last Affirmations Date`) and `!wrap` (`Last Vision Script Date`) to prevent same-day re-runs regardless of which command ran first. `working-day-gap` infers which weekdays a specific user tends to be active on from their session-log history (falling back to a standard Mon-Fri assumption below 10 logged sessions), then reports how many of *their* working days were actually missed since the last session — so `!morning`'s welcome-back message doesn't mistake a normal weekend for an absence, whether the user works a 5-day week, 7 days, or something else entirely.
