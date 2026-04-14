#!/usr/bin/env python3
"""Backfill data/events.json from the cached WordPress Tribe Events export.

Reads _migration/wp-events/all.json (fetched from the live WP JSON API) plus
the curated _migration/venue_photos.json and writes a clean data/events.json
suitable for the client-side calendar renderer on calendar.html.

Run: python3 _migration/scripts/backfill_from_wp.py
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WP_JSON = ROOT / "_migration" / "wp-events" / "all.json"
PHOTO_MAP = ROOT / "_migration" / "venue_photos.json"
OUT = ROOT / "data" / "events.json"


def clean_description(raw: str) -> str:
    """Strip Divi shortcodes and smart-quote-encoded markup from WP descriptions."""
    if not raw:
        return ""
    s = raw
    # Divi encodes shortcodes as [et_pb_*] with fancy quotes around attributes
    # and wraps most content in <p>…</p>. Strip the shortcodes first.
    s = re.sub(r"\[/?et_pb_[^\]]*\]", "", s)
    s = re.sub(r"\[/?[a-z_]+[^\]]*\]", "", s)
    # Collapse any empty paragraphs the shortcodes leave behind
    s = re.sub(r"<p>\s*</p>", "", s)
    # Decode HTML entities (&#8221; → ", &#038; → &, etc.)
    s = html.unescape(s)
    s = html.unescape(s)  # run twice for double-encoded strings
    # Drop paragraph tags but keep inline links and basic markup
    s = re.sub(r"</?p>", "\n", s)
    # Collapse whitespace
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def venue_record(raw_venue: dict, photo_map: dict) -> dict:
    if not raw_venue:
        return {}
    name = html.unescape(raw_venue.get("venue") or "")
    addr_parts = [
        raw_venue.get("address"),
        raw_venue.get("city"),
        raw_venue.get("state"),
        raw_venue.get("zip"),
    ]
    address = ", ".join(p for p in addr_parts if p)
    map_url = None
    if address:
        map_url = "https://maps.google.com/?q=" + address.replace(" ", "+")
    website = raw_venue.get("website") or None
    ebird_hotspot = website if website and "ebird.org/hotspot" in website else None
    return {
        "name": name,
        "address": raw_venue.get("address") or None,
        "city": raw_venue.get("city") or None,
        "state": raw_venue.get("state") or None,
        "zip": raw_venue.get("zip") or None,
        "map_url": map_url,
        "ebird_hotspot": ebird_hotspot,
        "website": website if not ebird_hotspot else None,
    }


def organizer_record(raw_org) -> dict | None:
    if not raw_org:
        return None
    if isinstance(raw_org, list):
        raw_org = raw_org[0] if raw_org else None
    if not raw_org:
        return None
    return {
        "name": raw_org.get("organizer") or None,
        "email": raw_org.get("email") or None,
        "phone": raw_org.get("phone") or None,
    }


def category_label(cats: list) -> str:
    """Map WP taxonomy to our three-way category."""
    names = {(c.get("name") or "").lower() for c in (cats or [])}
    if any("meeting" in n for n in names):
        return "meeting"
    if any("international" in n or "other local" in n for n in names):
        return "other"
    return "trip"


def main() -> None:
    events_raw = json.loads(WP_JSON.read_text())
    photo_map = json.loads(PHOTO_MAP.read_text())

    events = []
    for e in events_raw:
        venue_raw = e.get("venue") or {}
        if isinstance(venue_raw, list):
            venue_raw = venue_raw[0] if venue_raw else {}
        venue_name = venue_raw.get("venue") or ""

        # Photo cascade: WP's attached image if we have it locally,
        # else the venue's default photo from the curated map.
        photo = None
        img = e.get("image") or {}
        if isinstance(img, dict) and img.get("url"):
            wp_fn = img["url"].split("?")[0].rsplit("/", 1)[-1]
            # Stripped-suffix fallback for -scaled / -NxN
            local_dir = ROOT / "images"
            if (local_dir / wp_fn).exists():
                photo = f"images/{wp_fn}"
        if not photo:
            mapped = photo_map.get(venue_name)
            if mapped:
                photo = f"images/{mapped}"

        record = {
            "id": e.get("slug") or f"wp-{e.get('id')}",
            "title": html.unescape(e.get("title") or "").strip(),
            "start": e.get("start_date"),  # "YYYY-MM-DD HH:MM:SS" local
            "end": e.get("end_date"),
            "all_day": bool(e.get("all_day")),
            "timezone": e.get("timezone") or "America/New_York",
            "category": category_label(e.get("categories") or []),
            "description": clean_description(e.get("description") or ""),
            "leader": organizer_record(e.get("organizer")),
            "venue": venue_record(venue_raw, photo_map),
            "photo": photo,
            "ebird_link": (e.get("website") or None) if (e.get("website") or "").startswith("https://ebird") else None,
            "detail_url": e.get("url") or None,
            "source": {
                "type": "wp_tribe_events",
                "wp_id": e.get("id"),
                "imported_from": "menotomybirdclub.com/wp-json/tribe/events/v1",
            },
        }
        events.append(record)

    # Sort chronologically, ascending by start
    events.sort(key=lambda r: r["start"] or "")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(events, indent=2, ensure_ascii=False))
    print(f"wrote {len(events)} events → {OUT.relative_to(ROOT)}")

    # Quick sanity summary
    with_photo = sum(1 for r in events if r["photo"])
    with_leader = sum(1 for r in events if r["leader"] and r["leader"]["name"])
    print(f"  with photo:  {with_photo}/{len(events)}")
    print(f"  with leader: {with_leader}/{len(events)}")


if __name__ == "__main__":
    main()
