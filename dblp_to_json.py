#!/usr/bin/env python3
"""
Regenerate publications.json from a DBLP author page.

Usage
-----
    python3 tools/dblp_to_json.py                    # writes publications.json
    python3 tools/dblp_to_json.py --keep-preprints   # keep arXiv versions of published papers
    python3 tools/dblp_to_json.py --out /tmp/pubs.json

Why DBLP rather than a .bib file: DBLP's XML export is stable, has one
record per publication, and already distinguishes journal articles from
preprints. If you would rather curate the list by hand, just edit
publications.json directly; this script is a convenience, not a
dependency.

Stdlib only. No pip install needed.
"""

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

DBLP_PID = "163/3199"  # Lisa Raithel
ME = "Lisa Raithel"


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

def fetch_dblp(pid: str) -> ET.Element:
    """Download the DBLP XML record for one author and parse it."""
    url = f"https://dblp.org/pid/{pid}.xml"
    req = urllib.request.Request(url, headers={"User-Agent": "personal-site-builder"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return ET.fromstring(resp.read())


# --------------------------------------------------------------------------
# Mapping DBLP records to our JSON shape
# --------------------------------------------------------------------------

def classify(rec: ET.Element) -> str:
    """
    Turn a DBLP element tag into a short human-readable kind.

    DBLP marks preprints as <article publtype="informal">, which is how we
    tell an arXiv posting apart from a real journal article.
    """
    tag = rec.tag
    publtype = rec.get("publtype", "")

    if tag == "article":
        return "preprint" if publtype == "informal" else "journal"
    if tag == "inproceedings":
        return "conference"
    if tag == "phdthesis":
        return "thesis"
    if tag == "data":
        return "dataset"
    if tag == "proceedings":
        return "edited volume"
    return tag


def venue_of(rec: ET.Element) -> str:
    """Build a readable venue string: journal + volume, or booktitle + year."""
    journal = rec.findtext("journal")
    booktitle = rec.findtext("booktitle")
    volume = rec.findtext("volume")
    number = rec.findtext("number")
    year = rec.findtext("year", "")
    school = rec.findtext("school")

    if journal:
        vol = f" {volume}" if volume else ""
        num = f"({number})" if number else ""
        return f"{journal}{vol}{num}".strip()
    if booktitle:
        return f"{booktitle} {year}".strip()
    if school:
        return f"PhD thesis, {school}"
    return rec.findtext("publisher") or ""


def links_of(rec: ET.Element) -> list:
    """
    Collect external links. DBLP puts them in <ee>; we label them by host
    so the page shows "ACL Anthology" rather than a bare URL.
    """
    labels = [
        ("aclanthology.org", "ACL Anthology"),
        ("arxiv.org", "arXiv"),
        ("arXiv", "arXiv"),
        ("zenodo", "Zenodo"),
        ("ceur-ws.org", "PDF"),
        ("archives-ouvertes", "HAL"),
    ]
    out, seen = [], set()
    for ee in rec.findall("ee"):
        url = (ee.text or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        label = next((lab for key, lab in labels if key in url), "DOI")
        out.append({"label": label, "url": url})
    return out[:2]  # two links per entry is plenty


def normalise_title(title: str) -> str:
    """Lowercase, strip punctuation. Used to match a preprint to its paper."""
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def to_entry(rec: ET.Element) -> dict:
    title = (rec.findtext("title") or "").strip().rstrip(".")
    return {
        "title": title,
        "authors": [(a.text or "").strip() for a in rec.findall("author")],
        "venue": venue_of(rec),
        "year": int(rec.findtext("year", "0") or 0),
        "kind": classify(rec),
        "links": links_of(rec),
    }


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pid", default=DBLP_PID, help="DBLP person ID")
    ap.add_argument("--out", default="publications.json")
    ap.add_argument(
        "--keep-preprints",
        action="store_true",
        help="keep arXiv entries even when the paper also appeared at a venue",
    )
    args = ap.parse_args()

    root = fetch_dblp(args.pid)

    # Each publication sits inside an <r> wrapper; take its single child.
    entries = [to_entry(list(r)[0]) for r in root.findall("r") if len(r)]

    # Drop arXiv duplicates of papers that also have a venue entry.
    if not args.keep_preprints:
        published = {
            normalise_title(e["title"])
            for e in entries
            if e["kind"] not in ("preprint",)
        }
        entries = [
            e for e in entries
            if e["kind"] != "preprint" or normalise_title(e["title"]) not in published
        ]

    # Newest first; stable within a year.
    entries.sort(key=lambda e: -e["year"])

    payload = {
        "_comment": "Generated by tools/dblp_to_json.py. Hand edits will be overwritten.",
        "highlight": ME,
        "entries": entries,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(entries)} entries to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
