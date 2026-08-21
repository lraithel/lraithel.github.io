# lraithel.github.io

Personal academic site, built with Jekyll on the [minimal-mistakes](https://mmistakes.github.io/minimal-mistakes/)
theme (pulled in via `remote_theme`, not vendored). GitHub Pages builds and
publishes it automatically on every push to the default branch — there is
still no local build step required to *publish*, only to preview.

```
_config.yml                 site settings, author bio, nav
index.md                    the whole page: hero, research, publications, teaching, contact
_data/navigation.yml        top nav links
_data/publications.json     the publication list (edit this)
_sass/minimal-mistakes/skins/_custom.scss   the burgundy color palette
_sass/custom-site.scss      hero entity spans, research grid, publication list styling, dark mode
assets/css/main.scss        wires the two files above into the theme's build
tools/update_publications.py  merges new/updated publications from Semantic Scholar (runs weekly, see below)
tools/dblp_to_json.py       manual, full-regenerate DBLP import - not part of the automated pipeline
cv.pdf                      add your own
```

## Preview locally

Needs Ruby + Bundler (this needs installing once; nothing to install to just
publish).

```bash
bundle install
bundle exec jekyll serve
# open http://localhost:4000
```

If you hit `Invalid US-ASCII character` from Sass, your shell's locale isn't
UTF-8 — run with `LANG=C.utf8 LC_ALL=C.utf8 bundle exec jekyll serve` instead.

Always go through `http://localhost:4000`, never open `_site/index.html`
directly from disk. The theme links its CSS as `/assets/css/main.css` (root-
relative), which only resolves when served over HTTP — opened as a `file://`
URL it 404s silently and the page renders as unstyled HTML.

## Update the publication list

A scheduled GitHub Action (`.github/workflows/update-publications.yml`)
runs every Monday - and can be run on demand from the Actions tab
("Update publications" → "Run workflow") - to fetch from
[Semantic Scholar](https://www.semanticscholar.org/), merge in anything new,
and open a PR if there's a diff. It only adds new entries or fills in a
real venue for an entry that's currently listed as a bare arXiv preprint;
it never deletes anything, so entries Semantic Scholar doesn't index (the
PhD thesis, Zenodo datasets, CEUR workshop notes) are left alone. Review
the PR like any other before merging.

Why not Google Scholar: it has no API and blocks automated requests from
datacenter IPs almost immediately, GitHub Actions runners included -
scraping it isn't something that can run unattended.

To run it yourself:

```bash
python3 tools/update_publications.py --dry-run   # preview, writes nothing
python3 tools/update_publications.py             # writes _data/publications.json
```

`_data/publications.json` can also just be edited by hand at any time.
Jekyll picks up `_data/*.json` automatically — no separate build step.

`tools/dblp_to_json.py` still exists as a separate, manual tool, but DBLP's
coverage of recent workshop/shared-task papers has lagged, so it's no
longer part of the automated pipeline. It also *fully regenerates* the
file rather than merging, so running it will discard anything the workflow
above or hand-editing has added that DBLP doesn't know about.

