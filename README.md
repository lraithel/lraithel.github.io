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

Always go through `http://localhost:4000`, never open `_site/index.html`
directly from disk. The theme links its CSS as `/assets/css/main.css` (root-
relative), which only resolves when served over HTTP — opened as a `file://`
URL it 404s silently and the page renders as unstyled HTML.

## Update the publication list

Either edit `_data/publications.json` by hand, or pull the current state
from DBLP:

```bash
python3 tools/dblp_to_json.py
```

The script drops arXiv entries when the same paper also has a venue entry.
Pass `--keep-preprints` to keep both. It uses the standard library only.
Jekyll picks up `_data/*.json` automatically — no separate build step.

## Changing the color scheme

The accent color lives in `_sass/minimal-mistakes/skins/_custom.scss` as
`$primary-color` (plus a handful of derived variables). The three hero
entity-span colors (`$ent-source`, `$ent-method`, `$ent-eval`) live at the
top of `_sass/custom-site.scss`. Dark mode is hand-written in the
`@media (prefers-color-scheme: dark)` block at the bottom of that same
file — it has to live *after* the theme's own component styles are
imported (see the comment there) or the theme's unconditional colors win
the cascade tie and dark mode silently does nothing.

## Before you publish: things I could not fill in

- `cv.pdf` — add your own.
- Whether you want a photo. `_config.yml`'s `author.avatar` is unset; point
  it at an image under `assets/images/` and the sidebar picks it up.
- The research blurbs and the two organisation entries are drafts, but HeMAI
  and SMM4H-HeaRD both check out as public, so the workshop link is filled in.
- Pre-2023 publications were topped up by hand (LREC 2022 and a 2019 RepEval
  paper were missing) since `dblp.org` wasn't reachable from the sandbox
  this was edited in — run `tools/dblp_to_json.py` yourself to confirm
  against the current DBLP record and catch anything from before 2019.

## Design notes

The hero sentence is marked up as annotated spans with entity labels, which
is the one deliberate flourish on the page — now colored in shades of the
site's own burgundy accent rather than TU Berlin/DFKI brand colors. Dark
mode follows the system setting. Everything else leans on the theme:
the CV-style sidebar bio, the publication list grouped by year, and the
teaching/service list are custom content, laid out with the theme's own
typography and spacing.
