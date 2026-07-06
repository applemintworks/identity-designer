---
name: identity-workspace
description: Sets up and maintains the identity-designer workspace — the persistent file structure holding a user's identity profile, advisors, and history. Use when a user wants to set up a personal AI profile for the first time, re-onboard after a gap, migrate content from an old profile, or run a workspace health check. Triggers on commands !setup-identity, !refresh, !import-profile. Also use when someone mentions "super profile", "identity workspace", or wants Claude to build a living picture of who they are across sessions. Ships alongside identity-rituals (daily/session commands) and advisor-board (the board of advisors) — all three are part of one identity-designer plugin.
---

# Identity Workspace

Part of the **identity-designer** system — a personal identity design system built on ICM (Interpretable Context Methodology). This skill owns the workspace itself: detecting it, creating it, keeping it healthy, and migrating content into it. Daily and session rituals live in `identity-rituals`; the board of advisors lives in `advisor-board`.

**Core thesis:** Most AI profiles tell Claude what you do. This one tells Claude who you're becoming.

---

## File Structure

When fully set up, the workspace looks like this:

```
[workspace-name]/
├── CLAUDE.md                        ← Claude routing (auto-loads on session start)
├── GEMINI.md                        ← Gemini manual load instructions
├── AGENTS.md                        ← Cursor/Codex routing
├── index.md                         ← Hub: maps all files and their purpose
│
├── profile/
│   ├── identity.md                  ← values, work style, frictions, two-year self
│   ├── affirmations.md              ← 3–5 identity statements (pre-populated, customizable)
│   ├── advisors.md                  ← board of advisors with ~40-line profiles each
│   └── voice.md                     ← writing patterns, tone markers, communication style
│
├── system/
│   ├── memory.md                    ← hot memory: last session + ritual tracking dates, updated by !morning and !wrap
│   ├── signal-rules.md              ← pattern-matching rules for the signal layer
│   └── preferences.md               ← saved command preferences
│
├── library/
│   ├── rolodex.md                   ← relationship briefings for !rolodex (header-only stub at setup)
│   └── glossary.md                  ← domain terms/acronyms for Claude to reference (header-only stub at setup)
│
└── logs/
    ├── session-log-[year]-[q].md    ← raw session logs (quarterly, written at !wrap)
    └── achievement-log-[year].md    ← curated achievements (annual, auto-populated at !wrap)
```

`library/` starts with two stub files — a header explaining purpose, no data. Users fill them in over time, and can add more files here freely (client briefs, domain docs, anything else); the plugin doesn't prescribe the full contents, only seeds these two starting points.

---

## Modes

Detect which mode applies at the start of every interaction with this skill.

### Pre-Setup: Storage Check

The first thing `!setup-identity` does — before scanning for existing profiles — is check for cloud storage.

Check for the following in order:

**Google Drive Desktop**
- Windows: `G:\My Drive\`, `C:\Users\[name]\Google Drive\`
- Mac: `~/Google Drive/`, `~/Library/CloudStorage/GoogleDrive-[email]/`

**OneDrive**
- Windows: `C:\Users\[name]\OneDrive\`, `C:\Users\[name]\OneDrive - [CompanyName]\`
- Mac: `~/OneDrive/`, `~/OneDrive - [CompanyName]/`

**If Google Drive is found:** *"I can see Google Drive is installed — great. I recommend saving your workspace inside your Google Drive folder. This gives you automatic cloud backup and makes your profile portable across AI platforms like Gemini and ChatGPT. Does that work for you?"* If yes, use it as the workspace root. If no, ask for their preferred path and confirm before continuing.

**If OneDrive is found (but not Google Drive):** *"I can see OneDrive is installed — that works for cloud backup. One thing worth knowing: if you ever want to use your profile with Gemini or ChatGPT, Google Drive tends to be more portable. But OneDrive will absolutely work here. Want to save your workspace in OneDrive, or somewhere else?"*

**If both are found:** Recommend Google Drive for portability.

**If neither is found:** Offer both options in the same breath rather than stalling on one — *"I'd recommend Google Drive Desktop for automatic backup and cross-platform portability, worth installing if you don't have it. But no need to stop and set that up now — I can just start in a local folder, and you can move it into Drive whenever it's convenient."* If they want to install Drive first, pause and wait for confirmation before proceeding. Otherwise, ask for a local folder path and confirm before creating any files.

**Request direct filesystem access — don't just detect the app.** Immediately after the user confirms Google Drive or OneDrive as the storage choice, actively request direct folder/filesystem access to that location (Cowork's folder-access request, or the platform equivalent) before creating any files. Detecting that Google Drive Desktop or OneDrive is installed only confirms the *app* is present — it says nothing about *how* Claude will be writing to it in this session. Never rely on the user to self-diagnose which access mode is active; request the direct path explicitly, every time, as its own step.

**Why this matters:** a cloud-storage API connector (create/search/read-style tools) and direct filesystem access are not interchangeable, even though both can "reach" the same Drive or OneDrive folder. A connector typically supports creating files but not overwriting or deleting them in place. Since Drive allows duplicate filenames in one folder, a connector-based "update" to an existing file — `identity.md` after onboarding synthesis, or any `!wrap`/`!refresh` rewrite — doesn't overwrite anything. It silently creates a second file, and local sync clients disambiguate with a suffix like `(1)`, leaving the original placeholder untouched and the real content buried in a duplicate with no error or signal that anything went wrong.

**Where the API connector is still fine:** one-time reads of files identity-designer doesn't own, such as scanning an old profile during `!import-profile`. Never use it for profile/system files this plugin creates and rewrites every session — those always go through direct filesystem access, confirmed before the first file is created.

### First Run Detection

After the storage check, scan the workspace for signs of an existing profile:
- Check for content, not just filenames. A file called `context.md` is only a signal if it reads like a profile — references to the user's name, role, goals, or communication preferences.
- Strong indicators: `CLAUDE.md` with personal routing logic, files named `identity`, `profile`, or a person's name, folders named `me/`, `profile/`, or `workspace/` containing personal context.
- If found → **Existing Profile Mode**. If not → **Fresh Setup Mode**.

### Fresh Setup Mode

Triggered by `!setup-identity` with no existing profile detected.

1. Ask what to name the workspace folder. Default `my-workspace/`.
2. Create the full folder structure.
3. Populate all default files from `references/file-templates.md`.
4. Say the workspace is ready and profile-building takes ~20 minutes.
5. Run the **Onboarding Sequence**.

### Existing Profile Mode

Triggered when existing profile files are detected.

1. Tell the user what was found and that it will be left completely alone — identity-designer creates a fresh workspace alongside it. Let them know they'll have the option to run `!import-profile` once their new profile is set up, to bring over anything worth keeping.
2. Let the user name the new workspace or accept the default.
3. Create the full folder structure in the new root; populate default files from `references/file-templates.md`.
4. Run the **Onboarding Sequence** fresh — do not pre-populate answers from the old profile.
5. After onboarding, point to `!import-profile` for surgically bringing over specific pieces later.

**Non-destructive rule:** Never read from, write to, modify, or delete any files outside the new workspace root.

### Steady State

Every session after setup, `CLAUDE.md` loads `index.md`, then `profile/identity.md`, `system/memory.md`, and `system/signal-rules.md` — all three unconditional, since the signal layer needs `signal-rules.md` watching quietly all session, and `memory.md`'s Last Session and Ritual Tracking dates are what `!morning` and `!wrap` check against for same-day and gap detection. `profile/affirmations.md` loads only when `!morning`'s ritual actually runs — the first touch of the day; if `!morning` already ran earlier that day, the whole ritual (affirmations included) is skipped. `profile/voice.md` loads only for writing/drafting tasks; `profile/advisors.md` and `system/preferences.md` load only when a command needs them — `advisors.md` for `!supercharge`, `!ask-advisor`, `!ask-board`, `!add-advisor`, `!retire-advisor`, `!create-board`, or `!update-board`; `preferences.md` for any command capable of saving or reading a standing preference. `library/rolodex.md` loads only when `!rolodex` runs. `library/glossary.md` loads when the conversation touches on terms the user has defined there — not a mandatory per-session load, similar to `voice.md`. This happens regardless of which identity-designer skill ends up handling the turn. See `identity-rituals` for `!morning`, which runs the session-open ritual against that loaded context.

---

## Onboarding Sequence

Seven targeted questions that build a complete profile in one conversation (~20 minutes). Ask one at a time; briefly confirm what you heard before moving to the next.

Frame it first: *"I'd like to get to know you — not the resume version, the real one. I'll ask you 7 questions about how you think, work, and want to grow. There's no test or wrong answers — the only thing that makes this useful is your honesty. Take your time when answering, and we'll build something that actually sounds like you."*

1. *"What kind of work makes you lose track of time?"* → values, strengths, work style
2. *"What do people consistently come to you for that still surprises you a little?"* → blind-spot strengths
3. *"What's the thing you're most trying to stop doing or change about how you work?"* → friction, without a weakness-inventory feel
4. *"What would you do professionally if you knew you couldn't fail?"* → aspiration and fear
5. *"In two years, what would need to be true for you to feel like you nailed this chapter?"* → the two-year self
6. *"Who do you most want to think like — and what specifically about how they think?"* → seeds the board of advisors without announcing it
7. *"What do you want to be known for that you're not known for yet?"* → the identity gap

**On short or deflecting answers:** Don't re-prompt or push. Acknowledge warmly and move on — a partial profile built on honest answers beats a complete one built on performed ones.

**Work Context — one practical question, not part of the 7.** `identity.md`'s Work Context block is factual intake, not identity reflection, so it doesn't need one-at-a-time treatment, and it shouldn't feel like an 8th reflection question tacked onto the previous seven. Mark the shift explicitly before asking it — close out the reflection questions first, then flag this one as quick and different in kind: *"That's the reflection side done. One quick practical one before we move on — nothing to think hard about: what's your current role and organization, and what tools do you use day to day?"* Same tolerance for short or partial answers as above — fill in whatever's given, leave the rest as placeholder text rather than pushing for completeness.

**After the 7 questions (and Work Context):**
- Synthesize and write to `profile/identity.md`.
- Generate 3–5 personalized affirmations from the user's own words for `profile/affirmations.md`.
- If question 6 surfaced a specific person, offer to swap them into the advisor roster (this touches `advisor-board`'s territory — hand off the actual add via `!add-advisor`).
- Offer voice extraction from 2–3 pasted writing samples into `voice.md`.

**Optional: Connect your work tools.** After voice extraction (or if skipped), offer integrations as a distinct opt-in step: *"One more optional step — you can connect the tools you actually use for work, so I can automatically scan for achievement candidates at `!pulse` and `!wrap` instead of relying entirely on your recall. What tools do you use?"* Take whatever the user names — Jira, QuickBooks, a Notion CRM, Stripe, nothing at all — there's no fixed menu to choose from. For each tool, confirm scope explicitly: if it's one of the worked examples in `identity-rituals`'s "On integrations" rule (Slack, Asana/Monday/Jira, Confluence, GitHub, Google Drive), use that scoping; for anything else, ask directly what should count as achievement-worthy in that tool (completed tasks, closed deals, closed invoices — whatever fits) rather than guessing. Default both `!pulse` and `!wrap` to light mode (no scanning) with a 14-day lookback, then ask one line: *"I'll default to light mode with a 14-day lookback — want to customize that instead (deep scanning, different window, per-command settings)?"* Only walk through mode-per-command and lookback specifics if they say yes, and only mention the roughly 3–5x token cost if deep mode ends up selected. Save everything to `preferences.md` under `## Integration Preferences`. If the user says no to connecting tools at all, they can connect later by just asking.

---

## Commands

### !setup-identity
Runs install mode. See Pre-Setup: Storage Check, then Fresh Setup Mode or Existing Profile Mode above.

**Signals:** *"I want to set up a profile," "build my identity profile," "get started with identity designer," "create my personal AI profile."*

### !refresh

A compressed re-onboarding for when the profile feels stale, plus a full workspace health check.

1. Ask what's changed since setup — role, goals, or who they're becoming. Update `profile/identity.md`, especially the two-year self and affirmations.
2. **CLAUDE.md** — verify the `<!-- identity-designer: routing -->` section is intact. If it's grown significantly from other plugins writing to it, offer to tidy it (never touching content outside the identity-designer section without asking).
3. **Core profile files** — scan `identity.md`, `affirmations.md`, `advisors.md`, `voice.md` for anything unexpectedly empty, truncated, or off-purpose. Report, don't edit.
4. **System files** — check `memory.md`, `signal-rules.md`, `preferences.md` for structural integrity. Flag anomalies without touching them.
5. **index.md currency** — compare against what actually exists; offer to update if files were added or removed.
6. **Unrecognized content** — surface anything in a core file that looks externally added and doesn't match expected structure.

Keep the report short — a single summary with one "want me to clean this up?" offer, not an item-by-item interrogation.

**Signals:** *"my profile feels stale," "let's update my identity profile," "check my workspace health," "re-onboard me."*

### !import-profile

A surgical tool for bringing specific content from an old profile into the workspace. Never auto-populates; never touches source files.

**Scan mode** (`!import-profile` alone): find or ask where the old profile lives, map what's found against identity-designer's files, and ask per-piece whether to bring it in. Write only what's approved.

**Targeted mode** (`!import-profile [file or topic]`): read the named source, extract only what's relevant, propose exactly what would be written, wait for confirmation.

**When content doesn't map cleanly:** propose a new file rather than discarding it, and add an entry to `index.md` so it stays part of the workspace map.

**Rules:** read-only on source files; fresh onboarding answers take precedence over conflicting old content (flag conflicts, let the user decide); confirm before writing anything; can run any time after `!setup-identity`.

**Signals:** *"I want to import my profile," "migrate my old profile," "bring over my old profile."*

---

## Platform Support

The workspace is platform-agnostic — all data lives in the files, and routing files adapt per platform.

- **Claude** → reads `CLAUDE.md` automatically at session start
- **Cursor / Codex CLI** → reads `AGENTS.md` automatically
- **Gemini** → `GEMINI.md` holds manual load instructions (user uploads files at session start)
- **ChatGPT** → no auto-read; follow the same manual-load approach, or paste `profile/identity.md` into Custom Instructions for static persistent context

All routing files point to `index.md` first, which maps the full workspace for any AI to navigate.

**One caveat on portability:** `identity-rituals`'s `!morning`/`!wrap` same-day and working-day-gap checks are deterministic — they run the `date_check.py` script that ships inside `identity-rituals`'s own `scripts/` folder, via code execution where that's available (Claude Desktop, Cowork, Claude Code). On a platform without code execution, both commands fall back to comparing dates directly in prose (see each command's own fallback note in `identity-rituals/SKILL.md`) — same-day detection stays exact either way, but the working-day-gap estimate loses precision without the script's session-log inference.

---

## Behavioral Rules

**Confirm before writing to files.** Never silently update profile or system files. Tell the user what you wrote, or ask first.

**On CLAUDE.md as a shared file.** Other installed plugins may write to `CLAUDE.md`. Read the whole file at session start, but treat content outside `<!-- identity-designer: routing -->` as supplementary context, not routing instructions. Never delete or overwrite content outside that section.

**On workspace expansion.** The default file structure is a floor, not a ceiling. Treat unrecognized user-added files or folders as intentional. Read them if relevant to the task at hand. Never delete or modify them without explicit instruction; offer to add a useful one to `index.md`.

**On unrecognized content in core files.** If a core file contains content you didn't write and that doesn't match expected structure, don't delete it — flag it at the next `!refresh` instead.

**On command signals.** All three commands here write meaningfully to the workspace, so a matched signal phrase proposes the command rather than auto-running it — e.g. *"Sounds like you want to import your old profile — want me to run `!import-profile`?"* Never run silently just because a phrase matched.

---

## Reference Files

- `references/file-templates.md` — full default content for every file created at `!setup-identity`. Read during install mode before creating files. `profile/advisors.md`'s template pulls its starting roster from `advisor-board`'s `references/default-advisors.md` — both skills ship in the same plugin, so that file is available at setup time even though `advisor-board` owns the advisor commands.
