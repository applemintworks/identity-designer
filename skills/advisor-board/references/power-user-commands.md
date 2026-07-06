# Power-User Commands

Full procedures for `advisor-board`'s power-user-gated commands. All four are never proactively surfaced — offered or run only when a user explicitly asks. Read this file when one of `!add-role`, `!remove-role`, `!create-board`, or `!update-board` is actually invoked.

---

## Role Taxonomy

### !add-role

Power-user command for adding a custom role to the taxonomy, beyond the eight built-in ones — like `!create-board`, never proactively surfaced; only runs when a user explicitly asks.

1. Ask for the role name and a short description of the kind of thinking or decision it covers — parallel to an advisor's anchor sentence. This description becomes the role's "When to Use" text in the Advisor Index and what a user reads when deciding who, if anyone, to assign to it.
2. **Soft cap at 8, never a hard block.** If the roster is already at 8 roles or more, warn before proceeding: *"You're at [N] roles already — 8 is about where a role taxonomy stops being glanceable. I can still add [role name], but each additional role makes by-role invocation and quick scanning a little harder. Want to go ahead?"* Proceed on confirmation regardless of the count; this never refuses outright.
3. Add a new `##` section to `profile/advisors.md`, alphabetized among existing roles, seeded as a blank slot: `**Status:** No advisor currently assigned. Add one via \`!add-advisor\` — name "[Role]" as the role when prompted.`
4. Add the corresponding Advisor Index row (Name: *(unfilled)*, When to Use: the description from step 1), keeping the table's alphabetical-by-role order.
5. Confirm what was created.

**Signals:** *"I want to add a new role," "create a custom role for [X]," "add [role] as an option."* Never inferred from ordinary conversation — same gating as `!create-board`.

### !remove-role

Power-user command for removing a role from the taxonomy entirely — never proactively surfaced, same gating as `!add-role`.

1. Ask which role to remove.
2. **If an advisor currently holds it:** removing the role removes them from active rotation too, so treat this with the same care as `!retire-advisor`. Confirm explicitly: *"[Role] is currently held by [Name]. Removing the role archives them the same way `!retire-advisor` would — history stays, but they're out of rotation. Sound right? Or would you rather reassign [Name] to a different role first and keep them active?"* If reassignment is wanted, hand off to that instead of proceeding with removal.
3. **If the role is already blank:** no advisor is affected — just confirm the removal itself.
4. Delete the role's `##` section from `profile/advisors.md` entirely (not a blank-slot placeholder — this is a taxonomy change, not a departure) and remove its Advisor Index row.
5. **If this leaves fewer than 3 roles:** note it once, gently — *"That leaves you with [N] roles — worth knowing this narrows the categories your board is organized by. It doesn't touch `!ask-board`'s curation, which was never role-based to begin with."* Then proceed on confirmation; this never blocks.
6. Confirm what was removed.

**Signals:** *"remove the [role] role," "get rid of the [role] category," "I don't need a [role] role."*

---

## Board Organization

### !create-board

Power-user command for organizing a growing roster into named, purpose-specific groups — offer it per the trigger in `SKILL.md`'s "On multiple advisor boards" rule, rather than waiting to be asked by name.

1. Ask what to name the board. For a user's first board, suggest `core-advisors` as a sensible default — a naming suggestion only, not a reserved or special name. Fully renameable, and behaves no differently from any other board name.
2. Ask which advisors from `profile/advisors.md` belong on it. Any roster member can belong to zero, one, or several boards.
3. Create it in `profile/advisor-boards.md` (template in `identity-workspace`'s `references/file-templates.md`). Confirm what was created.

**Signals:** *"organize my advisors into groups," "create a board for [context]," "I want a separate board for [project]."*

### !update-board [instruction]

One flexible, natural-language command for editing board membership — `!update-board swap naval for mollick`, `!update-board remove brown`, `!update-board add topol to creative-strategy`. Replaces the older idea of a dedicated swap-only command.

**Which board:** if only one board exists, apply directly but state which board for transparency. If more than one exists, either the instruction names it explicitly or it's inferred from whichever board was just referenced in the conversation — confirm which board before writing either way.

**Scope:** only rearranges advisors already in `profile/advisors.md`. If a named replacement isn't in the roster yet, prompt to run `!add-advisor` first rather than creating them inline.

**"Remove" is ambiguous — always clarify.** "Remove Brown" could mean take her off this specific board only (she stays in the master roster, still reachable via `!ask-advisor`, `!supercharge`, and dynamic `!ask-board` curation) or retire her entirely. Ask which is meant unless it's unambiguous from context. Full retirement is always `!retire-advisor`'s job — never assume it here.

**No boards yet:** this command has nothing to operate on. A boardless user's swap- or removal-sounding request maps to `!retire-advisor` (to remove) or `!add-advisor` (to add) instead — offer to set up a board only if they seem to actually want one.

Confirm before writing, same as every other command touching `profile/advisors.md` or `profile/advisor-boards.md`.

**On phrasing patterns:** if a user's board-edit requests settle into a consistent personal shorthand across several invocations — their own words for swap/remove/add, not a prescribed vocabulary — offer to note it in `preferences.md` at the next `!wrap` session audit. This documents how *this* user phrases things; it never dictates the "correct" way to phrase a request.

**Signals:** *"swap [name] for [name] on my board," "remove [name] from this board," "add [name] to [board]."*
