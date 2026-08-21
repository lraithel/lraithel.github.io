#!/usr/bin/env python3
"""
Merge new or upgraded publications from Semantic Scholar into
_data/publications.json.

Usage
-----
    python3 tools/update_publications.py                    # updates _data/publications.json in place
    python3 tools/update_publications.py --dry-run           # print what would change, write nothing
    python3 tools/update_publications.py --author-id 12345   # skip the name-based lookup

Why Semantic Scholar rather than Google Scholar: Scholar has no API and
blocks automated requests almost immediately from datacenter IPs, GitHub
Actions runners included - scraping it is not something that can run
unattended. Semantic Scholar's Graph API is free, official, needs no API
key at this volume, and pairs each arXiv preprint with its published venue
when one exists, which is what lets this script fix the "Scholar still
lists it as arXiv" problem: an existing preprint-only entry gets upgraded
in place once a real venue shows up, instead of sitting there stale.

This script only *adds* new entries and *upgrades* existing preprint-only
entries once a venue appears for them - it never deletes or overwrites an
entry it can't find a confident match for. Things Semantic Scholar doesn't
index well (the PhD thesis, Zenodo datasets, CEUR workshop notes) are left
exactly as hand-curated. Run with --dry-run to preview, or let the
scheduled GitHub Action (.github/workflows/update-publications.yml) open a
PR so changes get reviewed before they go live.

dblp_to_json.py still exists as a separate, manual, full-regenerate tool -
running it will overwrite entries this script added that DBLP doesn't
know about, so it's no longer part of the automated pipeline.

Stdlib only. No pip install needed.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

ME = "Lisa Raithel"

# Set this once you've confirmed it (printed by every run, or check the
# scheduled workflow's log) to skip the name lookup and its ambiguity risk
# entirely. Overridable with --author-id or the S2_AUTHOR_ID env var.
AUTHOR_ID = None

AFFILIATION_HINTS = ("berlin", "dfki", "charit", "bifold", "saclay")

API_ROOT = "https://api.semanticscholar.org/graph/v1"
USER_AGENT = "lraithel-site-publications-bot (personal site build, https://lraithel.github.io)"

PAPER_FIELDS = "title,year,venue,publicationVenue,externalIds,authors,publicationTypes"


# --------------------------------------------------------------------------
# Semantic Scholar API
# --------------------------------------------------------------------------

def http_get_json(url: str, params: dict) -> dict:
    full_url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url, headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"gave up on {full_url} after retries")


def search_author(name: str) -> list:
    data = http_get_json(
        f"{API_ROOT}/author/search",
        {"query": name, "fields": "name,affiliations,paperCount"},
    )
    return data.get("data") or []


def resolve_author_id(explicit_id) -> str:
    if explicit_id:
        return explicit_id
    if os.environ.get("S2_AUTHOR_ID"):
        return os.environ["S2_AUTHOR_ID"]
    if AUTHOR_ID:
        return AUTHOR_ID

    candidates = search_author(ME)
    if not candidates:
        raise RuntimeError(f"No Semantic Scholar author found for {ME!r}")

    for c in candidates:
        affiliation = " ".join(c.get("affiliations") or []).lower()
        if any(hint in affiliation for hint in AFFILIATION_HINTS):
            return c["authorId"]

    # No affiliation matched (S2's affiliation data is patchy) - fall back
    # to whichever candidate has the most papers under that name.
    best = max(candidates, key=lambda c: c.get("paperCount") or 0)
    return best["authorId"]


def fetch_all_papers(author_id: str) -> list:
    papers, offset, limit = [], 0, 100
    while True:
        data = http_get_json(
            f"{API_ROOT}/author/{author_id}/papers",
            {"fields": PAPER_FIELDS, "offset": offset, "limit": limit},
        )
        batch = data.get("data") or []
        papers.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
        time.sleep(1)  # be polite, no API key means a shared rate limit
    return papers


# --------------------------------------------------------------------------
# Mapping Semantic Scholar records to our JSON shape
# --------------------------------------------------------------------------

def normalise_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def classify(paper: dict) -> str:
    ext = paper.get("externalIds") or {}
    pub_venue = paper.get("publicationVenue") or {}
    venue_name = (paper.get("venue") or "").strip()
    types = paper.get("publicationTypes") or []
    title_l = (paper.get("title") or "").lower()

    has_real_venue = bool(pub_venue) and venue_name.lower() != "arxiv.org"

    if not has_real_venue and ext.get("ArXiv"):
        return "preprint"
    if title_l.startswith("overview of") or "shared task" in title_l:
        return "shared task"
    if "JournalArticle" in types:
        return "journal"
    if "workshop" in venue_name.lower():
        return "workshop"
    return "conference"


def links_of(paper: dict, kind: str) -> list:
    ext = paper.get("externalIds") or {}
    links = []
    if ext.get("ACL"):
        links.append({"label": "ACL Anthology", "url": f"https://aclanthology.org/{ext['ACL']}/"})
    elif ext.get("DOI"):
        links.append({"label": "DOI", "url": f"https://doi.org/{ext['DOI']}"})
    if ext.get("ArXiv") and (kind == "preprint" or not links):
        links.append({"label": "arXiv", "url": f"https://doi.org/10.48550/arXiv.{ext['ArXiv']}"})
    return links[:2]


def format_authors(authors: list, limit: int = 8) -> list:
    names = [a.get("name", "").strip() for a in authors if a.get("name")]
    if len(names) > limit:
        return names[: limit - 1] + ["and others"]
    return names


def to_entry(paper: dict) -> dict:
    ext = paper.get("externalIds") or {}
    kind = classify(paper)
    year = paper.get("year") or 0
    venue_name = (paper.get("publicationVenue") or {}).get("name") or paper.get("venue") or ""

    if kind == "preprint" and ext.get("ArXiv"):
        venue = f"arXiv:{ext['ArXiv']}"
    elif year and str(year) not in venue_name:
        # Semantic Scholar's publicationVenue.name sometimes already ends
        # in the year (e.g. "LREC-COLING 2026") and sometimes doesn't
        # (e.g. "EACL") - only append it when it's not already there.
        venue = f"{venue_name} {year}".strip()
    else:
        venue = venue_name

    return {
        "title": (paper.get("title") or "").strip().rstrip("."),
        "authors": format_authors(paper.get("authors") or []),
        "venue": venue,
        "year": year,
        "kind": kind,
        "links": links_of(paper, kind),
    }


# --------------------------------------------------------------------------
# Merging into the existing, hand-curated list
# --------------------------------------------------------------------------

def arxiv_id_of_entry(entry: dict):
    haystack = entry.get("venue", "") + " " + " ".join(l["url"] for l in entry.get("links", []))
    m = re.search(r"(\d{4}\.\d{4,5})", haystack)
    return m.group(1) if m else None


def find_match(paper: dict, entries: list):
    s2_arxiv = (paper.get("externalIds") or {}).get("ArXiv")
    norm_title = normalise_title(paper.get("title") or "")

    for entry in entries:
        if s2_arxiv and s2_arxiv == arxiv_id_of_entry(entry):
            return entry
        entry_norm = normalise_title(entry["title"])
        if entry_norm == norm_title:
            return entry
        if SequenceMatcher(None, entry_norm, norm_title).ratio() > 0.92:
            return entry
    return None


def merge_paper(paper: dict, entries: list) -> tuple:
    """Returns (action, entry) where action is 'added', 'upgraded', 'skipped', or 'unchanged'."""
    if not paper.get("title") or not paper.get("year"):
        return "skipped", None

    match = find_match(paper, entries)
    new_entry = to_entry(paper)

    if match is None:
        entries.append(new_entry)
        return "added", new_entry

    if match.get("kind") == "preprint" and new_entry["kind"] != "preprint":
        match["venue"] = new_entry["venue"]
        match["kind"] = new_entry["kind"]
        seen = {l["url"] for l in new_entry["links"]}
        match["links"] = new_entry["links"] + [l for l in match.get("links", []) if l["url"] not in seen]
        match["links"] = match["links"][:2]
        return "upgraded", match

    return "unchanged", match


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--author-id", default=None, help="Semantic Scholar author ID (skips the name lookup)")
    ap.add_argument("--out", default="_data/publications.json")
    ap.add_argument("--dry-run", action="store_true", help="print what would change, write nothing")
    args = ap.parse_args()

    with open(args.out, encoding="utf-8") as f:
        payload = json.load(f)
    entries = payload["entries"]

    author_id = resolve_author_id(args.author_id)
    print(f"Semantic Scholar author ID: {author_id}", file=sys.stderr)

    papers = fetch_all_papers(author_id)
    print(f"Fetched {len(papers)} papers from Semantic Scholar", file=sys.stderr)

    counts = {"added": 0, "upgraded": 0, "unchanged": 0, "skipped": 0}
    changes = []
    for paper in papers:
        action, entry = merge_paper(paper, entries)
        counts[action] += 1
        if action in ("added", "upgraded"):
            changes.append(f"  {action}: {entry['title']} ({entry['year']})")

    print(
        f"{counts['added']} added, {counts['upgraded']} upgraded, "
        f"{counts['unchanged']} already up to date, {counts['skipped']} skipped",
        file=sys.stderr,
    )
    for line in changes:
        print(line, file=sys.stderr)

    if not changes:
        print("No changes.", file=sys.stderr)
        return 0

    if args.dry_run:
        print("Dry run - not writing.", file=sys.stderr)
        return 0

    entries.sort(key=lambda e: -e.get("year", 0))
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
