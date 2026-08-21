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
tools/dblp_to_json.py       regenerates _data/publications.json from DBLP
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

## Update the publication list

Either edit `_data/publications.json` by hand, or pull the current state
from DBLP:

```bash
python3 tools/dblp_to_json.py
```

The script drops arXiv entries when the same paper also has a venue entry.
Pass `--keep-preprints` to keep both. It uses the standard library only.
Jekyll picks up `_data/*.json` automatically — no separate build step.

