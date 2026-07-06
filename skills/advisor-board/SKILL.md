---
name: advisor-board
description: Manages the user's personal board of advisors — adding, retiring, organizing them into optional named boards, and consulting them individually or as a curated group. Also lets power users customize the role taxonomy itself. Use when a user wants to add someone to their board, retire an advisor, organize advisors into named groups, ask a specific advisor's opinion, get a curated panel's perspective on a decision, or add/remove a role category. Triggers on commands !add-advisor, !retire-advisor, !add-role, !remove-role, !create-board, !update-board, !ask-advisor, !ask-board. Also use when someone mentions "board of advisors", "advisor lens", or wants a second opinion filtered through a specific way of thinking. Ships alongside identity-workspace (setup) and identity-rituals (daily coaching, which draws on the board) — all three are part of one identity-designer plugin.
---

# Advisor Board

Part of the **identity-designer** system. Owns the board of advisors: adding, retiring, organizing them into optional named boards, and consulting them individually or in parallel. Workspace setup lives in `identity-workspace`; daily rituals live in `identity-rituals`.

**No tiers on the roster itself.** Every advisor in `profile/advisors.md` is simply "in the roster" or archived — there's no core/bench distinction. Named boards (below) are optional groupings layered on top; any roster member can belong to none, one, or several.

**Setup dependency:** `identity-workspace`'s `!setup-identity` populates `profile/advisors.md` from this skill's `references/default-advisors.md` at install time. Both skills ship in the same plugin, so the file is available even though the command that uses it lives elsewhere.

**Always read the live file.** Before applying any lens or making any change, read `profile/advisors.md` — never rely on the default descriptions in `references/default-advisors.md` once the user has customized their roster.

---

## Commands

### !add-advisor

Prompt for: name, role, and one sentence on why this person belongs on the team. That sentence anchors how their lens gets applied — it should capture what's distinctive about how they think, not just who they are.

**Role options:** read the live Advisor Index in `profile/advisors.md` for the current role list — eight roles (challenge, craft, financial, humanity, operator, risk, strategy, wildcard) ship by default, but power users may have added or removed roles via `!add-role`/`!remove-role` below. If a role is currently blank (a prior retirement, or a role added via `!add-role` with no advisor yet), write the new profile directly into that role's existing section, replacing the blank-slot placeholder, rather than appending a new one. If the user names a role that doesn't exist yet, offer to run `!add-role` first rather than inventing one inline.

Generate a ~40-line advisor profile using the format of any filled entry in `references/default-advisors.md`. **Show the generated profile and confirm before writing** — never append it silently. Once confirmed, write to `profile/advisors.md` (or fill an existing blank slot, per above).

If the user isn't sure which role to assign, offer to help place them based on why they want this person on the board.

**After writing the profile:** update the Advisor Index table at the top of `profile/advisors.md` to add or edit the corresponding row, keeping alphabetical order by role, then by name within a role. The table should never fall out of sync with the entries below it.

**Signals:** *"add someone to my board," "I want [name] as an advisor," "put [name] on my board."*

### !retire-advisor

Ask which advisor to retire, then confirm: *"I'll archive [name] permanently — history stays, but they're out of rotation everywhere. Sound right?"* Move the full entry to `## Archived Advisors` at the bottom of `profile/advisors.md`, with a datestamp and optional note. Never delete. This is the only way an advisor leaves active rotation entirely — removing someone from one named board without retiring them is `!update-board`'s job, not this command's (see below).

**If retiring an advisor leaves their role with no one assigned:** replace their entry with a blank-slot placeholder rather than leaving an empty header — `**Status:** No advisor currently assigned. Add one via \`!add-advisor\` — name "[Role]" as the role when prompted.` Update the Advisor Index table's row for that role to match (Name: *(unfilled)*, When to Use: `Add via \`!add-advisor\``).

**After retiring:** update the Advisor Index table — remove the retired advisor's row, or convert it to the blank-slot row above if their role is now empty.

**Signals:** *"retire [name] from my board," "remove [name] from my advisors permanently," "archive [name] as an advisor."*

### !add-role

Power-user command for adding a custom role to the taxonomy, beyond the eight built-in ones — never proactively surfaced; only runs when a user explicitly asks. Full procedure (soft-cap warning script, blank-slot seeding, Advisor Index update): see `references/power-user-commands.md`.

**Signals:** *"I want to add a new role," "create a custom role for [X]," "add [role] as an option."* Never inferred from ordinary conversation.

### !remove-role

Power-user command for removing a role from the taxonomy entirely — never proactively surfaced, same gating as `!add-role`. Full procedure (handling a still-filled role, the fewer-than-3-roles warning): see `references/power-user-commands.md`.

**Signals:** *"remove the [role] role," "get rid of the [role] category," "I don't need a [role] role."*

### !create-board

Power-user command for organizing a growing roster into named, purpose-specific groups — offer it per the trigger in "On multiple advisor boards" below, rather than waiting to be asked by name. Full procedure: see `references/power-user-commands.md`.

**Signals:** *"organize my advisors into groups," "create a board for [context]," "I want a separate board for [project]."*

### !update-board [instruction]

One flexible, natural-language command for editing board membership — `!update-board swap naval for mollick`, `!update-board remove brown`, `!update-board add topol to creative-strategy`. Full disambiguation rules (which board applies, scope limits, the "remove" ambiguity, no-boards-yet fallback, phrasing-pattern capture): see `references/power-user-commands.md`.

**Signals:** *"swap [name] for [name] on my board," "remove [name] from this board," "add [name] to [board]."*

### !ask-advisor

Invoke a specific advisor's lens on any topic or decision at any point in a session — without running the full `!supercharge` sequence.

**By name** (`!ask-advisor Andy Grove`): apply that advisor's lens directly.

**By role** (`!ask-advisor risk`): read the live Advisor Index in `profile/advisors.md` for the current role list — eight roles ship by default (challenge, craft, financial, humanity, operator, risk, strategy, wildcard), but the set may be customized via `!add-role`/`!remove-role`. Apply whoever currently holds that role.

**Zero or multiple holders for a role:** don't dead-end either way. If no one holds it (including a known blank slot), fall back to "by question" semantic matching below — find the best anchor-sentence fit, apply their lens, and say plainly what happened, e.g., *"Risk doesn't have an advisor yet — closest fit is [name], going with them. Want someone else, or help adding one via `!add-advisor`?"* If more than one holds it, pick whichever fits better against any live context and say so; with no disambiguating context, pick one, say so, and name the other as the alternative.

**By question** (`!ask-advisor [free-form question or topic]`): read the question, select the most contextually relevant advisor, state who and why, then respond through that lens.

**No argument** (`!ask-advisor`): ask *"What are you trying to think through?"* then select the optimal advisor based on the response.

**Rules:** always state who you're drawing from and why *before* responding — never make the selection invisible. One advisor per invocation; if several seem equally relevant, pick one and say so.

**Signals:** *"what would [advisor] think," "ask [advisor] about this," "get [advisor]'s take," "run this by [advisor]."* If a named person could plausibly be either a board advisor or a rolodex contact (see `identity-rituals`'s `!rolodex`), ask which is meant before responding.

### !ask-board

**No argument** (`!ask-board`): the universal default — works identically for every user regardless of tier. Curate the most contextually relevant advisors from the full roster in `profile/advisors.md`, up to 5, fewer if fewer exist — this cap holds regardless of how many roles or advisors are in the roster (eight ship by default; power users can add or remove roles via `!add-role`/`!remove-role` without affecting this cap or the curation logic below, since curation was never role-based). Favor distinct perspectives over raw relevance-ranking, so the panel doesn't end up with several advisors who'd all say essentially the same thing. Curation runs on each advisor's anchor sentence and "How They Think" section — the same basis `!ask-advisor` uses for lens application — never on the fixed role label (challenge/craft/financial/humanity/operator/risk/strategy/wildcard). The role tag never limits which topics an advisor can be curated for; a wildcard-tagged advisor with a demonstrated record of, say, financial thinking is just as eligible for a money-shaped question as anyone tagged financial. A blank role slot simply isn't in the candidate pool — no special handling needed, since curation was never role-based to begin with. State who was selected and briefly why before delivering the panel — the curation step is never invisible. This never falls back to a stored default board, even for power users who have one.

**With a board name** (`!ask-board [board]`, power users only): run that specific named board from `profile/advisor-boards.md` instead of curating fresh. Requires the board to already exist via `!create-board`. **If `profile/advisor-boards.md` doesn't exist yet, or no board matches the name given:** fall back to bare `!ask-board` curation and say so — e.g. *"You don't have a board called [name] yet — here's a curated panel instead. Want to set one up via `!create-board`?"*

Either way:
1. Each advisor responds independently, in a consistent format: **[Name] — [role]:** followed by 2–4 sentences in their voice, grounded in their anchor sentence and "How They Think" section.
2. After all advisors have responded, ask: *"Want a synthesis pulling these together?"* If yes, provide a 2–3 sentence synthesis that weighs where the advisors agree and where they genuinely diverge, rather than flattening the disagreement. No advisor is a permanent chairman by default; if a user wants one voice to always deliver the synthesis, let them designate it explicitly and note the preference in `preferences.md`.

**When to reach for this vs. `!ask-advisor`:** use `!ask-board` when the value is in seeing where perspectives conflict — a genuinely high-stakes or ambiguous call. For routine questions, a single advisor's lens via `!ask-advisor` is faster and usually sufficient.

**Signals:** *"ask the board," "what does my board think," "get a few perspectives on this," "run this by my advisors."*

---

## Behavioral Rules

**On advisor lenses.** Don't just change tone — change the type of thinking. Before applying any lens, read the live `profile/advisors.md`, specifically the anchor sentence and "How They Think" section — never the defaults in this skill's reference file once the roster is customized. The anchor sentence is the key: it captures what's distinctive about how that person thinks, not just who they are.

**On board membership changes.** Any swap/add/remove request against a specific board is `!update-board`'s job, never `!retire-advisor`'s, unless the user explicitly means full retirement — see `!update-board`'s disambiguation rule in `references/power-user-commands.md`. Don't guess; ask when it's unclear which is meant.

**On multiple advisor boards.** If a user has more than ~10 advisors, or asks about organizing advisors by context or project, offer `!create-board`. Boards are optional, named groupings — any roster member can belong to none, one, or several, and there's no default or "active" board. `!ask-advisor` and `identity-rituals`'s `!supercharge` always search the full master roster in `advisors.md` regardless of what boards exist; bare `!ask-board` always curates fresh from the full roster rather than falling back to a stored default. `!ask-board [board]` and `!update-board` are the only ways a specific named board comes into play, and both require naming it explicitly.

**On command signals.** `!add-advisor`, `!retire-advisor`, `!create-board`, and `!update-board` all write to `profile/advisors.md` or `profile/advisor-boards.md`, so a matched signal proposes the command rather than auto-running it. `!ask-advisor` and `!ask-board` are pure Q&A with no write — a matched signal can run directly. **Ambiguous names:** never guess whether a named person is a board advisor or a rolodex contact (see `identity-rituals`'s `!rolodex`) — ask.

**On the Advisor Index table.** `profile/advisors.md` opens with a summary table (Role, Name, When to Use) covering every entry below it. Whenever `!add-advisor`, `!retire-advisor`, `!add-role`, or `!remove-role` changes the roster, update this table in the same pass — it should never be left stale relative to the actual entries.

**On the role taxonomy.** Eight roles ship by default, but the taxonomy isn't fixed — power users can add or remove roles via `!add-role`/`!remove-role`, gated exactly like `!create-board`: never proactively surfaced, only on explicit request. Because `!ask-board` and `!ask-advisor`'s by-question mode curate on each advisor's anchor sentence rather than their role tag (see `!ask-board` above), changing the taxonomy never touches selection logic — it's a lightweight organizational layer, not something load-bearing. `!add-role`/`!remove-role` keep the Advisor Index table in sync in the same pass, same as `!add-advisor`/`!retire-advisor`.

---

## Reference Files

- `references/default-advisors.md` — 8 default advisor profiles (~40 lines each) spanning all eight built-in roles, the starting roster loaded into every new workspace at `!setup-identity`. Organized as an Advisor Index table followed by alphabetized role sections. Read when generating new advisor profiles via `!add-advisor`, or as the format template for what a complete profile looks like.
- `references/power-user-commands.md` — full procedures for `!add-role`, `!remove-role`, `!create-board`, and `!update-board`. Read whenever one of these four is actually invoked; none of them are needed for `!ask-advisor`/`!ask-board`, the two commands used every session.
