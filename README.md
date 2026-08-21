# lraithel.github.io

Personal academic site, built with Jekyll on the [minimal-mistakes](https://mmistakes.github.io/minimal-mistakes/)
theme (pulled in via `remote_theme`, not vendored). GitHub Pages builds and
publishes it automatically on every push to the default branch.

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


## Update the publication list

A scheduled GitHub Action (`.github/workflows/update-publications.yml`)
runs regularyl, and can be run on demand from the Actions tab
("Update publications" → "Run workflow") - to fetch from
[Semantic Scholar](https://www.semanticscholar.org/), merge in anything new,
and open a PR if there's a diff. It only adds new entries or fills in a
real venue for an entry that's currently listed as a bare arXiv preprint;
it never deletes anything, so entries Semantic Scholar doesn't index (the
PhD thesis, Zenodo datasets, CEUR workshop notes) are left alone. Review
the PR like any other before merging.

To run:

```bash
python3 tools/update_publications.py --dry-run   # preview, writes nothing
python3 tools/update_publications.py             # writes _data/publications.json
```

`_data/publications.json` can also just be edited by hand at any time.
Jekyll picks up `_data/*.json` automatically.


