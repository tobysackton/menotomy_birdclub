#!/usr/bin/env python3
"""Parse an arlingtonbirds trip-announcement email into event records.

Input:  plain text email body on stdin or as --file argument.
Output: JSON array of event records (same schema as data/events.json) on stdout.

The parser recognizes the bold-triple pattern that Paul Ippolito uses every
week:

    *Wednesday, April 15*
    *Brooks Estate, Medford*
    *Diana Fruguglietti 8:30 AM – 10:30 AM*

    Join us as we search for early spring migrants... Meet at 266 Grove St...
    Diana Fruguglietti diana.fru@gmail.com

Each matched block becomes one event. Blocks that do not match the pattern
(for example a club-meeting announcement with a different layout) are emitted
to stderr as "needs_review" so a human can hand-add them.

Run: python3 _migration/scripts/parse_email.py \
          --file _migration/inbox/2026-04-13.txt \
          --today 2026-04-14 \
          --thread-id 19d894618ebdcbcd
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Bold line: *text*  (Markdown asterisks surround the whole line)
BOLD = r"\*([^*\n]+)\*"

# "Wednesday, April 15" or "Tues, Apr 15" etc.
DATE_RE = re.compile(
    r"^\s*\*?\s*(?P<dow>Mon|Tue|Tues|Wed|Wednes|Thu|Thur|Thurs|Fri|Sat|Sun)[a-z]*,?\s+"
    r"(?P<month>[A-Z][a-z]+)\s+(?P<day>\d{1,2})\s*\*?\s*$",
    re.IGNORECASE,
)

# "Diana Fruguglietti 8:30 AM – 10:30 AM"  — leader then time range.
# Matches whether the bold span is the entire line or only the start of it,
# since Paul sometimes writes "*John Edmondson 7:00 AM – 9:00 AM *We'll..."
# with description text following on the same line.
LEADER_TIME_RE = re.compile(
    r"\*?\s*(?P<leader>[A-Z][A-Za-z.' -]+?(?:\s+[A-Z][A-Za-z.' -]+){1,3})\s+"
    r"(?P<start>\d{1,2}(?::\d{2})?\s*[APap][Mm])\s*[–\-−—]\s*"
    r"(?P<end>\d{1,2}(?::\d{2})?\s*[APap][Mm])\s*\*?",
)

# Club meeting layout: second bold line is a time/status header such as
# "*6:30 PM Social Time, 7:00 Meeting Start*". Third bold line carries the
# meeting title, often "<Title> <Speaker> – <Venue>, <City>". Note the start
# time has no AM/PM in Paul's emails — we assume PM for meeting headers.
MEETING_HEADER_RE = re.compile(
    r"(?P<doors>\d{1,2}(?::\d{2})?\s*[APap][Mm])\s+(?:Social|Doors).*?"
    r"(?P<start>\d{1,2}(?::\d{2})?)\s*(?:[APap][Mm])?\s+Meeting",
    re.IGNORECASE,
)

EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")


def parse_time(s: str) -> tuple[int, int]:
    s = s.strip().upper().replace(" ", "")
    m = re.match(r"(\d{1,2})(?::(\d{2}))?(AM|PM)$", s)
    if not m:
        raise ValueError(f"bad time: {s}")
    h = int(m.group(1))
    mm = int(m.group(2) or 0)
    if m.group(3) == "PM" and h != 12:
        h += 12
    if m.group(3) == "AM" and h == 12:
        h = 0
    return h, mm


def resolve_year(month: int, day: int, today: date) -> int:
    """Event year = current year, unless that date is in the past and the next
    year gives a future date within 11 months."""
    year = today.year
    try:
        cand = date(year, month, day)
    except ValueError:
        return year
    if cand < today - (today - today):  # identical to cand < today but keeps mypy happy
        pass
    if cand < today:
        # next year
        year += 1
    return year


def clean_block_text(lines: list[str]) -> str:
    joined = "\n".join(lines).strip()
    # Drop enclosing asterisks from bold spans and normalize
    joined = re.sub(r"\*([^*\n]+)\*", r"\1", joined)
    joined = re.sub(r"\n{3,}", "\n\n", joined)
    return joined.strip()


def slug(title: str, start: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{start[:10]}-{base}"[:80].strip("-")


def parse(text: str, today: date, thread_id: str | None, sender: str | None) -> tuple[list[dict], list[str]]:
    # Normalize line endings and drop Google Group unsubscribe footer
    text = text.replace("\r\n", "\n")
    cutoff = text.find("-- \nGroup home page")
    if cutoff == -1:
        cutoff = text.find("--\nGroup home page")
    if cutoff != -1:
        text = text[:cutoff]
    lines = text.split("\n")

    events: list[dict] = []
    review: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        m_date = DATE_RE.match(line)
        if not m_date:
            i += 1
            continue
        # Expect: next non-blank bold line = location, following bold line = leader + time
        j = i + 1
        while j < n and not lines[j].strip():
            j += 1
        if j >= n:
            i += 1
            continue
        loc_line = lines[j].strip()
        if not (loc_line.startswith("*") and loc_line.endswith("*")):
            # Unexpected — record for review
            review.append(f"unmatched location line after {line!r}: {loc_line!r}")
            i = j
            continue
        location = loc_line.strip("*").strip()

        k = j + 1
        while k < n and not lines[k].strip():
            k += 1
        if k >= n:
            review.append(f"no leader/time line for {location!r}")
            i = k
            continue

        # Two possible layouts for the line after the location:
        #   A) leader + time range   (a field trip)
        #   B) meeting header        (a club meeting)
        leader_line = lines[k]
        m_leader = LEADER_TIME_RE.search(leader_line)
        m_meeting = MEETING_HEADER_RE.search(location) if not m_leader else None

        # Meeting header can also appear on the "location" bold line itself,
        # as it does in Paul's emails: the 2nd bold line is the time header
        # and the 3rd bold line is the actual title. Detect that case.
        if MEETING_HEADER_RE.search(location):
            # "location" is actually the meeting time header. The real title
            # lives on the next bold line (at index k).
            meeting_time_line = location
            # Gather one or more bold lines for the title (Paul sometimes
            # wraps the long title across two bold spans on consecutive lines)
            title_lines: list[str] = []
            kk = k
            while kk < n:
                cur = lines[kk].strip()
                if cur.startswith("*") and cur.endswith("*"):
                    title_lines.append(cur.strip("*").strip())
                    kk += 1
                elif cur.startswith("*") and not cur.endswith("*"):
                    # Multiline bold: collect until closing *
                    title_lines.append(cur.lstrip("*").strip())
                    kk += 1
                    while kk < n and not lines[kk].rstrip().endswith("*"):
                        if lines[kk].strip():
                            title_lines.append(lines[kk].strip())
                        kk += 1
                    if kk < n:
                        title_lines.append(lines[kk].rstrip().rstrip("*").strip())
                        kk += 1
                    break
                else:
                    break
            title = " ".join(title_lines).strip()
            # Meeting time parse. The meeting start time is bare ("7:00"
            # with no AM/PM); assume PM.
            mh = MEETING_HEADER_RE.search(meeting_time_line)
            try:
                raw_start = mh.group("start")
                if not re.search(r"[APap][Mm]", raw_start):
                    raw_start = raw_start + " PM"
                sh, smm = parse_time(raw_start)
            except Exception:
                review.append(f"meeting time parse failed: {meeting_time_line!r}")
                i = kk
                continue
            # Default a 90-minute meeting duration
            eh, emm = (sh + 1, smm + 30)
            if emm >= 60:
                eh += 1; emm -= 60

            # Meeting venue: usually the substring after " – " on the title line
            mvenue = None
            if "–" in title:
                _, _, after = title.rpartition("–")
                mvenue = after.strip().rstrip("*")
                title = title[:title.rfind("–")].strip().rstrip("*")

            # Description
            desc_start = kk
            desc_end = desc_start
            while desc_end < n:
                if DATE_RE.match(lines[desc_end].strip()):
                    break
                desc_end += 1
            description = clean_block_text(lines[desc_start:desc_end])

            month = MONTHS[m_date.group("month").lower()]
            day = int(m_date.group("day"))
            year = resolve_year(month, day, today)
            start_dt = datetime(year, month, day, sh, smm)
            end_dt = datetime(year, month, day, eh, emm)
            start_s = start_dt.strftime("%Y-%m-%d %H:%M:%S")
            end_s = end_dt.strftime("%Y-%m-%d %H:%M:%S")

            record = {
                "id": slug(title or "mbc-meeting", start_s),
                "title": title or "MBC Monthly Meeting",
                "start": start_s,
                "end": end_s,
                "all_day": False,
                "timezone": "America/New_York",
                "category": "meeting",
                "description": description,
                "leader": None,
                "venue": {
                    "name": mvenue or "Jenks Center",
                    "address": "109 Skillings Road" if (mvenue or "").startswith("Jenks") else None,
                    "city": "Winchester" if (mvenue or "").startswith("Jenks") else None,
                    "state": "MA",
                    "zip": "01890" if (mvenue or "").startswith("Jenks") else None,
                    "map_url": None,
                    "ebird_hotspot": None,
                    "website": None,
                },
                "photo": None,
                "ebird_link": None,
                "detail_url": None,
                "source": {
                    "type": "arlingtonbirds_email",
                    "gmail_thread_id": thread_id,
                    "sender": sender,
                    "imported_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                },
            }
            events.append(record)
            i = desc_end
            continue

        if not m_leader:
            review.append(f"unmatched leader/time line for {location!r}: {lines[k]!r}")
            i = k
            continue

        leader_name = m_leader.group("leader").strip()
        try:
            sh, smm = parse_time(m_leader.group("start"))
            eh, emm = parse_time(m_leader.group("end"))
        except ValueError as exc:
            review.append(f"bad time for {location!r}: {exc}")
            i = k
            continue

        # Description: remainder of the leader line (if any) plus following
        # lines until the next date heading
        leader_tail = leader_line[m_leader.end():].strip().lstrip("*").strip()
        desc_start = k + 1
        desc_end = desc_start
        while desc_end < n:
            nxt = lines[desc_end].strip()
            if DATE_RE.match(nxt):
                break
            desc_end += 1
        desc_lines = lines[desc_start:desc_end]
        if leader_tail:
            desc_lines = [leader_tail] + desc_lines
        description = clean_block_text(desc_lines)

        # Leader email: first @ in the description
        emails = EMAIL_RE.findall(description)
        leader_email = emails[0] if emails else None

        # Resolve dates
        month = MONTHS[m_date.group("month").lower()]
        day = int(m_date.group("day"))
        year = resolve_year(month, day, today)
        start_dt = datetime(year, month, day, sh, smm)
        end_dt = datetime(year, month, day, eh, emm)

        start_s = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        end_s = end_dt.strftime("%Y-%m-%d %H:%M:%S")

        record = {
            "id": slug(location, start_s),
            "title": location,
            "start": start_s,
            "end": end_s,
            "all_day": False,
            "timezone": "America/New_York",
            "category": "trip",
            "description": description,
            "leader": {
                "name": leader_name,
                "email": leader_email,
                "phone": None,
            },
            "venue": {
                "name": location,
                "address": None,
                "city": None,
                "state": "MA",
                "zip": None,
                "map_url": None,
                "ebird_hotspot": None,
                "website": None,
            },
            "photo": None,  # resolved later against venue_photos.json
            "ebird_link": None,
            "detail_url": None,
            "source": {
                "type": "arlingtonbirds_email",
                "gmail_thread_id": thread_id,
                "sender": sender,
                "imported_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            },
        }
        events.append(record)
        i = desc_end

    return events, review


def resolve_photos(events: list[dict]) -> None:
    """Apply the curated venue → photo map to email-sourced events.

    Uses fuzzy matching because email location strings are free-form ('Brooks
    Estate, Medford') while the WP venue names may differ slightly ('Brooks
    Estate'), sometimes with typos ('Arlington Resevoir')."""
    import difflib
    pm_path = ROOT / "_migration" / "venue_photos.json"
    if not pm_path.exists():
        return
    pmap: dict[str, str] = json.loads(pm_path.read_text())

    def norm(s: str) -> str:
        s = re.sub(r"[^a-z0-9]+", " ", s.lower())
        return re.sub(r"\s+", " ", s).strip()

    normalized = {norm(k): v for k, v in pmap.items()}

    def find_photo(candidate: str) -> str | None:
        c = norm(candidate)
        if not c:
            return None
        # exact
        if c in normalized:
            return normalized[c]
        # substring either direction
        for k, v in normalized.items():
            if k and (k in c or c in k):
                return v
        # fuzzy (handles 'Arlington Reservoir' vs WP's 'Arlington Resevoir')
        best = difflib.get_close_matches(c, normalized.keys(), n=1, cutoff=0.82)
        if best:
            return normalized[best[0]]
        return None

    for ev in events:
        if ev.get("photo"):
            continue
        # try title first, then venue name
        candidates = [ev.get("title")]
        venue = ev.get("venue") or {}
        if venue.get("name"):
            candidates.append(venue["name"])
        for cand in candidates:
            photo = find_photo(cand or "")
            if photo:
                ev["photo"] = f"images/{photo}"
                break


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=Path, help="path to email body text")
    ap.add_argument("--today", default=date.today().isoformat(),
                    help="reference date for year resolution (YYYY-MM-DD)")
    ap.add_argument("--thread-id", default=None)
    ap.add_argument("--sender", default=None)
    ap.add_argument("--out", type=Path, default=None,
                    help="write JSON to this file instead of stdout")
    args = ap.parse_args()

    if args.file:
        text = args.file.read_text()
    else:
        text = sys.stdin.read()

    today = datetime.strptime(args.today, "%Y-%m-%d").date()
    events, review = parse(text, today, args.thread_id, args.sender)
    resolve_photos(events)

    out = {"events": events, "needs_review": review}
    payload = json.dumps(out, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(payload)
        print(f"wrote {len(events)} events, {len(review)} needs-review → {args.out}",
              file=sys.stderr)
    else:
        print(payload)
    if review:
        print(f"-- needs_review: {len(review)} --", file=sys.stderr)
        for r in review:
            print("  ", r, file=sys.stderr)


if __name__ == "__main__":
    main()
