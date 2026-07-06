# Changelog

All notable changes to **identity-designer** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] — Initial Release

### Added
- Guided onboarding — a short intake builds your `identity.md` profile: who you are, what you're working toward, your voice, and your work context.
- Personal board of advisors — a default roster of eight perspectives (challenge, craft, financial, humanity, operator, risk, strategy, wildcard), fully customizable. Add, retire, or organize advisors into named boards for different contexts. Power users can also customize the role taxonomy itself — add or remove roles beyond the eight defaults via `!add-role`/`!remove-role`.
- Ask your board — get one advisor's take, or a curated panel's, on any decision.
- Daily and session rituals — a session-open check-in, sprint-aligned pulse reviews, and an end-of-session wrap that logs what happened.
- Rolodex — a quick relationship briefing before any meeting: what they know you for, what you want from the relationship, how things last stood.
- Achievement log → Growth Summary — turn logged work into a concise update for a manager or board, or a fuller case for a promotion or funding conversation.
- Optional integrations, configured at setup based on the tools you actually use.
- First executable script (`identity-rituals/scripts/date_check.py`), replacing LLM date-arithmetic with deterministic checks: same-day detection for `!morning`/`!wrap` (affirmations and vision scripting each fire once per day regardless of how many sessions happen, or in what order), and a working-day-aware absence check that infers each user's actual working pattern (5-day week, 7-day week, or otherwise) from their session-log history, so `!morning`'s welcome-back message doesn't mistake a normal weekend for an absence.
