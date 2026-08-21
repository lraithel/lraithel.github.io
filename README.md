# lraithel.github.io

Personal academic site. Static HTML, CSS and one small JavaScript file. No Jekyll,
no build step, no dependencies.

```
index.html            page content
assets/style.css      all styling
assets/pubs.js        renders publications.json
publications.json     the publication list (edit this)
tools/dblp_to_json.py regenerates publications.json from DBLP
cv.pdf                add your own
```

## Publish

Copy these files into the repo root, commit, push. GitHub Pages serves
`lraithel.github.io` from the default branch automatically once a user site repo
contains an `index.html`. Check Settings, Pages if it does not appear within a
minute or two.

## Preview locally

`fetch()` does not work over `file://`, so serve the folder:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Update the publication list

Either edit `publications.json` by hand, or pull the current state from DBLP:

```bash
python3 tools/dblp_to_json.py
```

The script drops arXiv entries when the same paper also has a venue entry. Pass
`--keep-preprints` to keep both. It uses the standard library only.

## Before you publish: things I could not fill in

- `REPLACE@ME.de` in the contact section
- Google Scholar profile URL in the hero links
- `cv.pdf`
- HeMAI workshop URL in the teaching section
- Whether you want a photo. The layout has room for one to the right of the hero
  text; say the word and I will add it.
- The research blurbs and the two organisation entries are drafts. Check that
  everything named there is public. I deliberately left out anything that looked
  like an unannounced proposal or grant.
- Pre-2023 publications are incomplete. Running the DBLP script fixes that.

## Design notes

The hero sentence is marked up as annotated spans with entity labels, which is
the one deliberate flourish on the page. Entity colours are the TU Berlin and
DFKI brand values, so the site matches your slides and posters. Dark mode follows
the system setting. Everything else is intentionally quiet.
