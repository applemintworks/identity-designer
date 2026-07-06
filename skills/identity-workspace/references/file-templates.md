# File Templates

This file contains the default content for every file created during `!setup-identity`. During install mode, read this file and use these templates to populate the workspace. Replace `[placeholders]` with actual values where indicated.

---

## CLAUDE.md

```markdown
<!-- identity-designer: routing -->
# [Workspace Name] — Claude Routing

At the start of every session, read `index.md` before responding to anything.

Then load:
- `profile/identity.md` — always
- `profile/affirmations.md` — only when !morning's ritual actually runs (first touch of the day — skipped, along with the rest of the ritual, if already run today)
- `profile/advisors.md` — only when a command needs it (!supercharge, !ask-advisor, !ask-board, !add-advisor, !retire-advisor, !create-board, !update-board)
- `profile/voice.md` — only when the task involves writing or drafting content
- `system/memory.md` — always (Last Session and Ritual Tracking dates feed !morning/!wrap's same-day and gap checks)
- `system/signal-rules.md` — always (watch for patterns throughout session)
- `system/preferences.md` — when a saved-preference command is invoked
- `profile/advisor-boards.md` — only if the file exists and a command names a specific board (!ask-board [board], !update-board, !create-board); there's no default board to read at session start
- `library/rolodex.md` — only when !rolodex runs
- `library/glossary.md` — only when the conversation touches on terms defined there; not a mandatory per-session load

This workspace runs the identity-designer plugin (identity-workspace, identity-rituals, advisor-board skills). Follow all behavioral rules in those skills.

Session open ritual: run !morning — check memory.md's Ritual Tracking > Last Affirmations Date → if today, skip the ritual entirely and begin work → otherwise, check Last Session Date for a working-day gap → display affirmations → ask the two questions → begin work.
Session close ritual: run !wrap before ending any session — vision scripting checks its own Last Vision Script Date and skips only that step if already run today; the rest of !wrap always runs.
<!-- /identity-designer -->
```

---

## GEMINI.md

```markdown
# [Workspace Name] — Gemini Load Instructions

Gemini doesn't auto-load files, so upload these at the start of each session:

1. `index.md`
2. `profile/identity.md`
3. `profile/affirmations.md`
4. `profile/advisors.md`
5. `profile/voice.md` (only if you'll be drafting content)
6. `system/memory.md`
7. `system/signal-rules.md`
8. `system/preferences.md`
9. `library/rolodex.md` (only if you use !rolodex)
10. `library/glossary.md` (only if you've added terms to it)

Then say: "You are my identity-designer assistant. Read the files I've uploaded and follow the instructions in index.md."

All routing logic and ritual behavior are defined in `index.md` and the plugin's skills, not here — this file exists only because Gemini requires a manual upload step. Once the files are uploaded, everything works exactly as it would on any other platform.

All profile data lives in these files. The system is fully portable — your data travels with you. One practical note specific to Gemini: it doesn't persist file writes back to your device automatically, so if you don't re-upload a current `system/memory.md` at the start of your next session, affirmations and vision scripting will simply re-run rather than silently failing. Not broken, just less precise than on a platform with persistent file access.
```

---

## AGENTS.md

```markdown
# [Workspace Name] — Agent Routing (Cursor / Codex / Generic)

At the start of every session, read `index.md` before responding to anything.

Then load:
- `profile/identity.md` — always
- `profile/affirmations.md` — only when !morning's ritual actually runs (first touch of the day)
- `profile/advisors.md` — only when a command needs it (!supercharge, !ask-advisor, !ask-board, !add-advisor, !retire-advisor, !create-board, !update-board)
- `profile/voice.md` — only for writing or drafting tasks
- `system/memory.md` — always (Last Session and Ritual Tracking dates feed !morning/!wrap's same-day and gap checks)
- `system/signal-rules.md` — always
- `system/preferences.md` — when a saved-preference command is invoked
- `library/rolodex.md` — only when !rolodex runs
- `library/glossary.md` — only when the conversation touches on terms defined there

This workspace runs the identity-designer system. Follow the behavioral rules described in `index.md`.
```

---

## index.md

```markdown
# [Workspace Name] — Index

This is the hub for your identity-designer workspace. Every platform routing file (CLAUDE.md, GEMINI.md, AGENTS.md) points here first.

## What This Workspace Does

Builds a living profile of who you're becoming — not just what you do. Three core incentives:
- **Career utility**: achievement log compiles into brief-ready language for a growth summary, via `!write-brief`
- **AI fluency**: daily coaching builds AI literacy through self-development
- **Daily ritual**: morning affirmations + evening vision scripting anchor identity every session

## File Map

### Profile (Layer 3 — stable identity)
- `profile/identity.md` — values, work style, frictions, two-year self. Load every session.
- `profile/affirmations.md` — identity statements. Load only when !morning's ritual runs (first touch of the day) — see CLAUDE.md for details.
- `profile/advisors.md` — board of advisors. Load only when a command needs it — see CLAUDE.md for the list.
- `profile/voice.md` — writing voice and communication style. Load for writing tasks only.

### System (Layer 3 — configuration)
- `system/memory.md` — hot memory: last session block + last !pulse date. Read at session open for drift detection.
- `system/signal-rules.md` — pattern-matching rules. Load every session, watch quietly.
- `system/preferences.md` — saved command preferences. Load when a command is invoked.

### Library (Layer 3 — user-owned reference material)
- `library/rolodex.md` — relationship briefings, read by !rolodex. Header-only stub at setup; filled in by the user over time.
- `library/glossary.md` — domain terms and acronyms for Claude to reference. Header-only stub at setup; filled in by the user over time.
- Add other files here freely — client briefs, domain docs, anything else. Not prescribed by the plugin.

### Logs (Layer 4 — accumulating artifacts)
- `logs/session-log-[year]-[q].md` — raw session log. Written by Claude at !wrap. New file each quarter.
- `logs/achievement-log-[year].md` — curated achievements. Written by Claude at !wrap. New file each year.

## Commands
- `!setup-identity` — initial install or re-setup *(identity-workspace)*
- `!refresh` — compressed re-onboarding + workspace health check *(identity-workspace)*
- `!import-profile` — surgically bring content from an old profile into this workspace *(identity-workspace)*
- `!morning` — session open ritual: affirmations + radar *(identity-rituals)*
- `!supercharge` — daily coaching: one insight, one action, one reflection *(identity-rituals)*
- `!wrap` — session close: vision scripting, logs, session audit, signal check *(identity-rituals)*
- `!pulse` — weekly or biweekly reflection: themes, achievement candidates, one question ahead *(identity-rituals)*
- `!write-brief` — compile achievement log into a growth summary *(identity-rituals)*
- `!rolodex` — pre-meeting relationship briefing from your rolodex *(identity-rituals)*
- `!add-advisor` — add an advisor to the roster *(advisor-board)*
- `!retire-advisor` — archive an advisor permanently *(advisor-board)*
- `!add-role` — add a custom role to the taxonomy (power users) *(advisor-board)*
- `!remove-role` — remove a role from the taxonomy (power users) *(advisor-board)*
- `!create-board` — create a named board (power users) *(advisor-board)*
- `!update-board` — swap, add, or remove board members via natural language (power users) *(advisor-board)*
- `!ask-advisor` — invoke an advisor's lens by name, role, or free-form question *(advisor-board)*
- `!ask-board` — curate the most relevant advisors on one question, or run a named board *(advisor-board)*

## Setup Date
[Date]

## Last Refreshed
[Date]
```

---

## profile/identity.md

```markdown
# Identity

*Generated: [date]*
*Last refreshed: [date]*

---

## Who I Am

[Populated during onboarding from question 1 — work that creates flow state]

## Strengths (Known)

[Populated during onboarding from question 2 — what people come to me for]

## Friction Points

[Populated during onboarding from question 3 — what I'm working to change]

## Aspirational Self

[Populated during onboarding from question 4 — what I'd do if I couldn't fail]

## Two-Year Self

[Populated during onboarding from question 5 — what needs to be true in two years]

## Identity Gap

[Populated during onboarding from question 7 — what I want to be known for that I'm not known for yet]

---

## Work Context

**Current role:** [role]
**Organization:** [org]
**Primary tools:** [tools]
```

---

## profile/affirmations.md

```markdown
# My Identity Affirmations

These statements define who you are becoming — not who you hope to be someday.
Read them at the start of each session. Update them as you grow.

*Pre-populated defaults. Replace with your own after onboarding, or keep any that already resonate.*

Generated: [date]
Last refined: [date]

---

I question assumptions, including my own. That's how I stay sharp.

I am building skills that compound. Every session makes the next one more valuable.

I bring irreplaceable judgment, context, and relationships to my work. AI amplifies this.

I protect my attention and direct it toward what matters most.

I am becoming someone with specific knowledge that is rare, valuable, and mine.
```

---

## profile/advisors.md

```markdown
# Board of Advisors

My advisors, each chosen to cover a distinct dimension of thinking. Everyone here is equally "in rotation" — there's no tiering on this list itself; !ask-board curates whichever are most relevant to a given question, and !supercharge draws from all of them for daily coaching.

*Eight roles pre-loaded, all filled by default advisors. Customize who fills each role via !add-advisor and !retire-advisor — retiring an advisor leaves their role as a blank slot rather than removing the role entirely. Customize the roles themselves — add a new one or remove one — via !add-role and !remove-role (power users). Once the list grows, !create-board lets you organize advisors into optional named groups without removing anyone from this master list.*

---

[Copy only the Advisor Index table and the eight role sections (## Challenge through ## Wildcard, each with its full ### Name — Title profile) from advisor-board's `references/default-advisors.md`. Do not copy that file's own H1 or preamble — this template already has its own title and intro above, so copying both produces two competing H1s. Do not copy its `## Archived Advisors` section — that documents this plugin's own development history, not anything the new user has done, and would seed a fresh workspace with an advisor nobody retired.]
```

---

## profile/advisor-boards.md

*Power user file — created via `!create-board`, typically offered once a roster passes ~10 advisors or the user asks about organizing them. Not part of default setup.*

```markdown
# Advisor Boards

This file organizes your advisor roster into optional named boards for different contexts.
There's no default or "active" board — !ask-board [board] and !update-board always name the board they mean.
Every advisor here still lives in profile/advisors.md and remains available via !ask-advisor, !supercharge, and dynamic !ask-board curation regardless of board membership.

---

## Boards

### core-advisors
- [Name] (role)
- [Name] (role)
- [Name] (role)
- [Name] (role)
- [Name] (role)

### creative-projects
- [Name] (role)
- [Name] (role)
- [Name] (role)
- [Name] (role)
- [Name] (role)

### technical-strategy
- [Name] (role)
- [Name] (role)
- [Name] (role)
- [Name] (role)
- [Name] (role)

### productivity-gurus
- [Name] (role)
```

---

## profile/voice.md

```markdown
# Voice Profile

*Generated: [date]*
*Last updated: [date]*

This file defines how I write and communicate. Claude reads this file when drafting emails, documents, or any written content on my behalf.

---

## Tone

[Populated during voice extraction — e.g., "direct and warm, not casual"]

## Sentence Style

[Populated during voice extraction — e.g., "short declarative sentences, rarely uses passive voice"]

## Vocabulary

[Populated during voice extraction — e.g., "plain words preferred, no jargon for its own sake"]

## What I Avoid

[Populated during voice extraction — e.g., "corporate hedging, starting sentences with 'It is important to note that'"]

## Opening Patterns

[Populated during voice extraction — how I typically open emails and documents]

## Closing Patterns

[Populated during voice extraction — how I typically close]

## Examples

[Paste 2-3 writing samples here, or leave for voice extraction during onboarding]

---

*This file grows over time as Claude learns more about how you write.*
```

---

## system/memory.md

```markdown
# Memory

*This file is managed by Claude — do not edit manually. The Last Session block is overwritten at every `!wrap`. The Ritual Tracking block is written independently by `!morning` and `!wrap`, each immediately after its own ritual runs — not deferred to session close, so same-day re-runs are detected correctly regardless of which command ran first.*

---

## Last Session

**Date:** [date]
**Key focus:** [what we worked on]
**Key insight:** [most important thing that came up]
**Reflection left open:** [the closing question from !supercharge or !wrap vision scripting]
**Achievements logged:** [yes/no — and what was added if yes]
**Signal fired:** [yes/no — and what was observed if yes]

---

## Ritual Tracking

**Last Affirmations Date:** [date — written by !morning right after affirmations are delivered]
**Last Vision Script Date:** [date — written by !wrap right after vision scripting runs]

---

## Last !pulse

**Date:** [date — updated after every !pulse run]
**Cadence:** [weekly / biweekly — set at first !pulse, saved in preferences.md]
```

---

## system/signal-rules.md

```markdown
# Signal Rules

Claude reads this file at every session start and watches for these patterns quietly throughout the session. At !wrap, surface at most one observation if a rule fires. Keep it to one sentence. Frame as a noticing, not a verdict.

---

## Active Rules

**Strength Pattern**
If a strength is mentioned 3+ times across sessions that doesn't appear in profile/identity.md:
→ "I keep hearing [X] come up in our conversations. It's not in your profile yet — want me to add it?"

**Goal Silence**
If a goal or theme from the two-year self hasn't appeared in 3+ sessions:
→ "[X] hasn't come up in a while — still on your radar?"

**Friction Pattern**
If the same friction or blocker appears across multiple sessions:
→ "I've been noticing [pattern] come up across a few sessions. Worth naming it?"

**Uncaptured Achievement**
If the user describes something notable they did or led that isn't in the achievement log:
→ "What you just described belongs in your achievement log. Want me to add it?"

**Blind Spot Strength**
If the user demonstrates a capability they didn't mention in onboarding:
→ "You just did something worth noting — [observation]. That's a strength you didn't mention. Want to add it?"

**Pulse Cadence**
If !pulse hasn't been run within the user's cadence window (check preferences.md for weekly or biweekly):
→ "We haven't done a !pulse check-in recently — want to do a quick one before we close?"

**Brief Cadence Approaching**
If today's date is within 2 weeks of the next-brief date in preferences.md:
→ "Your check-in period is ending soon — want to do a quick !refresh → !pulse → !write-brief run to close it out?"
Fire once per cycle — note it in the session log so it doesn't repeat. After !write-brief completes, offer to update the next-brief date in preferences.md for the next cycle.

**Voice Profile Missing**
If profile/voice.md still contains only default template content after 3+ sessions:
→ "Your voice profile is still at the default — want to paste a few writing samples so I can build it out?"
Fire this once only — note it in the session log so it doesn't repeat.

---

## Notes

- Never fire more than one signal per session
- Signal only at !wrap, never mid-session
- Add new rules here anytime via the session audit at !wrap
```

---

## system/preferences.md

```markdown
# Saved Preferences

This file stores saved defaults for commands that support shorthand invocation. Claude reads this file when a command is invoked.

---

## !morning Preferences

*(Saved after first use if the user establishes a standing answer or asks to skip part of the ritual)*

## !supercharge Preferences

*(Saved after first use — context, preferred advisor, delivery format)*

## !wrap Preferences

**staging:** false
*(Set to true to enable draft review before Claude writes to memory.md and session log. Power users only. Change anytime by asking Claude to "turn off staging at wrap".)*

## !pulse Preferences

**cadence:** [weekly / biweekly — set at first !pulse run]

## Brief Cadence

**brief-cadence:** [monthly / quarterly / semi-annual / annual / other — set at first !write-brief]
**next-brief:** [date — updated after each !write-brief run]

## !write-brief Preferences

*(Saved after first use)*

## Integration Preferences

**token-warning-acknowledged:** [yes — set at setup if user connected any tools]

### Connected tools
*(Each line is a tool the user connected at setup or added later — any tool they named, not a fixed list. Remove a line to disconnect.)*
*(e.g.: asana, slack, github, quickbooks, hubspot, a notion crm)*

### !pulse integrations
**mode:** light  *(light = no integration scan / deep = scan connected tools)*
**active:** [comma-separated list of tools to include when mode is deep]
**lookback:** 14 days

### !wrap integrations
**mode:** light  *(light = no integration scan / deep = scan connected tools)*
**active:** [comma-separated list of tools to include when mode is deep]
**lookback:** since-last-session

---

*This file is written by Claude, not by the user. Update via session audit at !wrap or by asking Claude directly.*
```

---

## library/rolodex.md

```markdown
# Rolodex

This file holds notes on people you want context on before meeting, calling, or reconnecting with — clients, partners, stakeholders, anyone whose relationship you're actively managing.

Not auto-populated. Add entries yourself, or let Claude create one the first time you run `!rolodex [name]` for someone new. `!rolodex` reads this file to deliver a quick briefing: what they know you for, what you want from the relationship, and your last interaction and its outcome.

---

*(Empty. Entries will appear here as you add contacts.)*
```

---

## library/glossary.md

```markdown
# Glossary

This file holds domain-specific terms, acronyms, and internal language relevant to your work — anything you'd want Claude to understand without re-explaining it each time.

Not auto-populated. Add terms yourself as they come up. Claude reads this file for context whenever the conversation touches on terms defined here.

---

*(Empty. Add terms as they come up.)*
```
