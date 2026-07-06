# Integration Scoping Rules

Detailed per-tool behavior for `!pulse` and `!wrap` when running in `deep` mode. Read this file only when deep-mode integration scanning actually applies — `light` mode (the default) skips integration scanning entirely and never needs this file.

---

Triggered, never continuous — read only when `!pulse` or `!wrap` actually runs, never passively, never at session open, never between commands. Always read-only, always scoped to what the user personally authored or completed within the lookback window — never in-progress work, never content authored by or assigned to others. There's no fixed app roster (see `identity-workspace`'s open-ended tool discovery at `!setup-identity`); these are worked examples of the pattern, not an exhaustive list:

- **Slack** — messages sent by the user, plus messages where the user is mentioned in a recognition or feedback context. Not DMs by default.
- **Asana / Monday / Jira** — completed tasks and closed tickets authored by the user, within the lookback window only.
- **Confluence / Google Drive** — documents authored by the user, primarily for voice extraction.
- **GitHub** — merged PRs and closed issues authored by the user, not all commits.

For any tool without a worked example — QuickBooks, HubSpot, a Notion CRM, whatever the user actually named at setup — don't guess at scope. Ask directly what should count as achievement-worthy in that tool, then apply the same general principles above to whatever they specify.

Never store raw content from a connected tool — surface candidates only, and always confirm with the user before writing anything to the achievement log. Per-command preferences live in `preferences.md` under `## Integration Preferences`; natural-language overrides ("quick pulse," "deep wrap," "skip Slack this time") apply per-run and revert to saved defaults afterward. Token cost runs roughly 3–5x higher per command when integrations are active, depending on activity volume and tools connected — users are told this at setup, so don't apologize for it when integrations run as configured.
