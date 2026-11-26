# lraithel.github.io

Personal academic site, built with Jekyll on the [minimal-mistakes](https://mmistakes.github.io/minimal-mistakes/)
theme (pulled in via `remote_theme`, not vendored). GitHub Pages builds and
publishes it automatically on every push to the default branch.

```
_config.yml                 site settings, author bio, nav
index.md                    the whole page: hero, research, publications, talks, teaching, contact
_data/navigation.yml        top nav links
_data/publications.json     the publication list (GENERATED, do not edit)
_data/talks.yml             the talk list (GENERATED, do not edit)
_sass/minimal-mistakes/skins/_custom.scss   the burgundy color palette
_sass/custom-site.scss      hero entity spans, research grid, publication list styling, dark mode
assets/css/main.scss        wires the two files above into the theme's build
```

## Preview locally

Needs Ruby + Bundler (this needs installing once; nothing to install to just
publish).

```bash
bundle install
bundle exec jekyll serve
# open http://localhost:4000
```


## Update publications and talks

`_data/publications.json` and `_data/talks.yml` are generated from the private
repo `lraithel/CV_long` (`data/publications.bib` and `data/talks.yml`), which
also feeds the CVs. Do not edit them here: change the data there and run

```bash
python3 tools/build_data.py --website ../lraithel.github.io
```

in the CV repo, then commit the two files in `_data/` here. A monthly scheduled
task does this automatically and opens a PR on both repos when something changed.
The previous weekly Semantic Scholar workflow is retired.
