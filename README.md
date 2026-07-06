# identity-designer

A personal identity design system for Claude. Most AI profiles tell Claude what you do — this one tells Claude who you're becoming. It builds a living, cross-session profile of your values, work style, and goals, gives you a customizable board of advisors to think alongside, runs daily/weekly rituals that turn ordinary sessions into a compounding record, and compiles that record into finished documents (a growth summary, a case for advancement, a pre-meeting briefing) when you need them.

Built for anyone who wants Claude to know them over time, not just per-conversation — regular employees, executives, and business owners alike.

Version 1.0.0 — initial public release.

---

## Install

This is a skills-only plugin — no bundled MCP server, no special permissions required. One nuance: the daily-ritual date checks in `identity-rituals` run a small Python script for accuracy, which needs code execution (available in Claude Desktop, Cowork, and Claude Code). On platforms without it — Gemini, ChatGPT — those specific checks fall back to reasoning through dates directly; everything else in the plugin is unaffected.

**For most people (Claude Desktop or Cowork):** download the `.zip` file and either drag it directly into a chat and say "install this plugin," or upload it via the file picker. No terminal or Claude Code CLI needed.

**Claude Code CLI**, for anyone testing from the terminal instead:

```
claude --plugin-dir ./identity-designer   # quick local test, no install
```

Run `/reload-plugins` to activate it if Claude Code was already running.

**Note:** always distribute the `.zip`, not the `.plugin` file — Claude Desktop's uploader currently only accepts `.zip`.

Once active, run `!setup-identity` to build your workspace. Setup takes about 20 minutes and walks through a short onboarding conversation.

---

## What's inside

Three skills, working together as one system:

**identity-workspace** — sets up and maintains the workspace itself: the file structure, onboarding, health checks, and migrating in content from an old profile.
`!setup-identity` · `!refresh` · `!import-profile`

**identity-rituals** — the recurring cadence: session-open and session-close rituals, daily coaching, periodic reflection, turning your achievement log into a finished document, and pre-meeting relationship briefings.
`!morning` · `!wrap` · `!supercharge` · `!pulse` · `!write-brief` · `!rolodex`

**advisor-board** — your board of advisors: adding and retiring them, organizing them into optional named boards, consulting them individually or as a curated panel, and — for power users — customizing the role categories themselves.
`!add-advisor` · `!retire-advisor` · `!add-role` · `!remove-role` · `!create-board` · `!update-board` · `!ask-advisor` · `!ask-board`

All commands also respond to natural language — you don't have to remember exact syntax. Say what you mean ("let's wrap up," "ask the board," "help me make a case for promotion") and Claude will recognize the intent. Full phrasing lists live in each skill's `SKILL.md`.

---

## Workspace file structure

`!setup-identity` creates this structure (defaults to your Google Drive if found, for cross-platform portability):

```
[workspace-name]/
├── CLAUDE.md / GEMINI.md / AGENTS.md   ← platform routing
├── index.md                            ← hub, maps every file
├── profile/                            ← identity, affirmations, advisors, voice
├── system/                             ← memory, signal rules, preferences
├── library/                            ← rolodex.md + glossary.md stubs; open-ended beyond that
└── logs/                               ← session logs + achievement log
```

Everything under `profile/` and `system/` is either generated during onboarding or maintained by Claude with your confirmation. `library/` starts with two header-only stubs and is otherwise yours to fill in or extend.

---

## A note on the default advisors

The starting board of eight advisors (Paul Graham, Cal Newport, Warren Buffett, Brené Brown, Brad Jacobs, Daniel Kahneman, Andy Grove, Naval Ravikant) are original summaries of each person's publicly known thinking, written to give the board a distinct starting point. They are not affiliated with, endorsed by, or created in consultation with any of these individuals, and every advisor — default or custom — can be edited, replaced, or retired at any time via `!retire-advisor` and `!add-advisor`. The eight role categories they fill (challenge, craft, financial, humanity, operator, risk, strategy, wildcard) can also be customized by power users via `!add-role` and `!remove-role`.

---

## Integrations

There's no fixed list of tools this plugin connects to. At setup, it asks what you actually use for work and scopes itself to that — read-only, and only when `!pulse` or `!wrap` actually runs, never continuously. See `identity-rituals/SKILL.md`'s "On integrations" for the full behavior.

---

## Privacy

Your profile is a plaintext record of your values, goals, relationships, and work history — worth saying plainly how it's handled. Everything lives in files you control; nothing is transmitted to Anthropic, this plugin's author, or anywhere else. If you store your workspace in Google Drive or OneDrive (recommended for cross-platform portability), your data inherits whatever security and sharing settings already apply to that account.

---

## License

Apache License 2.0 — see `LICENSE`.

## Changelog

See `CHANGELOG.md` for what's shipped.
