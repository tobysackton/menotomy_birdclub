#!/usr/bin/env python3
"""Merge a parsed-email JSON file into data/events.json.

Deduplicates on event id. If an incoming event has the same id as an existing
one, the incoming wins (so re-running the email parser with corrections
updates the canonical file). Output is sorted by start date.

Run: python3 _migration/scripts/merge_events.py _migration/inbox/2026-04-13-parsed.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVENTS = ROOT / "data" / "events.json"


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: merge_events.py <parsed.json> [<parsed.json> ...]", file=sys.stderr)
        sys.exit(2)

    existing = json.loads(EVENTS.read_text()) if EVENTS.exists() else []
    by_id = {e["id"]: e for e in existing}
    added = updated = 0

    for path in sys.argv[1:]:
        payload = json.loads(Path(path).read_text())
        new_events = payload.get("events", []) if isinstance(payload, dict) else payload
        for ev in new_events:
            if ev["id"] in by_id:
                by_id[ev["id"]] = ev
                updated += 1
            else:
                by_id[ev["id"]] = ev
                added += 1

    merged = sorted(by_id.values(), key=lambda r: r["start"] or "")
    EVENTS.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
    print(f"merged: +{added} new, {updated} updated, total={len(merged)}")


if __name__ == "__main__":
    main()
