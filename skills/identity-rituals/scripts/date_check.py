#!/usr/bin/env python3
"""
date_check.py — deterministic date/cadence helpers for identity-rituals.

Claude reasoning through date arithmetic in prose is unreliable. This script
replaces that reasoning for two specific checks:

  1. same-day       — has a ritual already run today? (used by !morning for
                       affirmations, and by !wrap for vision scripting)
  2. working-day-gap — how many of the user's actual working days have been
                       missed since their last session? (used by !morning's
                       welcome-back message, so a normal Friday-to-Monday
                       turnaround isn't mistaken for an absence)

Working-day inference reads session-log history to figure out which weekdays
this specific user tends to be active on, rather than assuming Mon-Fri for
everyone — a business owner working 7 days a week has no "weekend gap" to
account for, and the script should reflect that once there's enough history
to tell.

Usage:
  python date_check.py same-day <stored_date> <today>
  python date_check.py working-day-gap <last_session_date> <today> <session_log_dir>

All dates in YYYY-MM-DD format.
"""

import sys
import os
import re
from datetime import datetime, timedelta

# Below this many distinct logged session dates, there isn't enough history
# to reliably infer a working-day pattern, so fall back to the safe default.
# 10 is roughly two weeks of a 5-day-a-week user, or 10 days of a 7-day-a-week
# user — enough spread either way to start showing a real pattern.
MIN_SESSIONS_FOR_INFERENCE = 10

# Safe default for users with insufficient history: standard Mon-Fri.
# Python's date.weekday(): Monday=0 ... Sunday=6.
DEFAULT_WORKING_DAYS = {0, 1, 2, 3, 4}

DATE_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})", re.MULTILINE)


def parse_date(s):
    return datetime.strptime(s.strip(), "%Y-%m-%d").date()


def same_day(stored, today):
    """Return True if two YYYY-MM-DD strings represent the same calendar day."""
    try:
        return parse_date(stored) == parse_date(today)
    except ValueError:
        # Malformed or missing stored date (e.g. first-ever run) — treat as
        # "not today" so the ritual runs rather than silently failing shut.
        return False


def find_session_dates(log_dir):
    """Scan session-log-*.md files in log_dir for '## YYYY-MM-DD' headings."""
    dates = []
    if not os.path.isdir(log_dir):
        return dates
    for fname in os.listdir(log_dir):
        if fname.startswith("session-log-") and fname.endswith(".md"):
            path = os.path.join(log_dir, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except OSError:
                continue
            for m in DATE_HEADING_RE.finditer(content):
                try:
                    dates.append(parse_date(m.group(1)))
                except ValueError:
                    continue
    return sorted(set(dates))


def infer_working_days(log_dir):
    """Return (set_of_weekdays_worked, has_enough_history)."""
    dates = find_session_dates(log_dir)
    if len(dates) < MIN_SESSIONS_FOR_INFERENCE:
        return DEFAULT_WORKING_DAYS, False

    weekday_counts = {i: 0 for i in range(7)}
    for d in dates:
        weekday_counts[d.weekday()] += 1

    avg_weekday_rate = sum(weekday_counts[i] for i in range(5)) / 5.0

    working_days = set()
    for i in range(5):
        if weekday_counts[i] > 0:
            working_days.add(i)
    for i in (5, 6):
        # Count a weekend day as "working" only if activity on it is at least
        # half the average weekday rate — occasional weekend catch-up work
        # shouldn't flip the whole inference, but a genuinely 7-day pattern
        # will clear this easily.
        if avg_weekday_rate > 0 and weekday_counts[i] >= avg_weekday_rate * 0.5:
            working_days.add(i)

    if not working_days:
        working_days = DEFAULT_WORKING_DAYS

    return working_days, True


def working_day_gap(last_date_str, today_str, log_dir):
    today = parse_date(today_str)
    try:
        last = parse_date(last_date_str)
    except ValueError:
        # No valid last-session date yet — e.g. memory.md still has the
        # literal "[date]" placeholder because this is the first-ever
        # !morning after setup. Report unknown rather than crashing.
        return {
            "working_day_gap": None,
            "calendar_gap": None,
            "inferred_from_history": False,
            "working_days_used": sorted(DEFAULT_WORKING_DAYS),
            "first_run": True,
        }

    working_days, has_history = infer_working_days(log_dir)

    gap = 0
    d = last + timedelta(days=1)
    while d < today:
        if d.weekday() in working_days:
            gap += 1
        d += timedelta(days=1)

    return {
        "working_day_gap": gap,
        "calendar_gap": (today - last).days,
        "inferred_from_history": has_history,
        "working_days_used": sorted(working_days),
        "first_run": False,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: date_check.py <same-day|working-day-gap> ...", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "same-day":
        if len(sys.argv) != 4:
            print("Usage: date_check.py same-day <stored_date> <today>", file=sys.stderr)
            sys.exit(1)
        print("yes" if same_day(sys.argv[2], sys.argv[3]) else "no")

    elif cmd == "working-day-gap":
        if len(sys.argv) != 5:
            print(
                "Usage: date_check.py working-day-gap <last_session_date> <today> <session_log_dir>",
                file=sys.stderr,
            )
            sys.exit(1)
        result = working_day_gap(sys.argv[2], sys.argv[3], sys.argv[4])
        if result.get("first_run"):
            print("working_day_gap=unknown (no valid last-session date — likely first run)")
        else:
            print(f"working_day_gap={result['working_day_gap']}")
            print(f"calendar_gap={result['calendar_gap']}")
            print(f"inferred_from_history={result['inferred_from_history']}")
            print(f"working_days_used={result['working_days_used']}")

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
