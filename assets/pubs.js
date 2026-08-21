/* -------------------------------------------------------------------
   Renders publications.json into #pub-list, grouped by year.

   Deliberately dependency-free and framework-free: the whole point of
   a GitHub Pages site is that it keeps working in five years without a
   build step. Edit publications.json, push, done.
   ------------------------------------------------------------------- */

(function () {
  "use strict";

  const mount = document.getElementById("pub-list");
  if (!mount) return;

  // Escape anything that lands in innerHTML. The JSON is ours, but this
  // keeps a stray "&" or "<" in a title from breaking the markup.
  const esc = (s) =>
    String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));

  // "A", "A and B", "A, B and C"
  function formatAuthors(authors, highlight) {
    const names = authors.map((a) =>
      a === highlight ? `<span class="me">${esc(a)}</span>` : esc(a)
    );
    if (names.length <= 1) return names.join("");
    return names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
  }

  function renderEntry(p, highlight) {
    const links = (p.links || [])
      .map((l) => `<a href="${esc(l.url)}">${esc(l.label)}</a>`)
      .join("");

    return `
      <div class="pub">
        <span class="pub-title">${esc(p.title)}${
          p.kind ? `<span class="kind">${esc(p.kind)}</span>` : ""
        }</span>
        <span class="pub-authors">${formatAuthors(p.authors || [], highlight)}</span>
        <span class="pub-venue"><em>${esc(p.venue || "")}</em></span>
        ${links ? `<span class="pub-links">${links}</span>` : ""}
      </div>`;
  }

  function render(data) {
    const highlight = data.highlight || "";

    // Group by year, newest first. Entries keep their order within a year,
    // so the JSON itself controls what appears at the top of each block.
    const byYear = new Map();
    for (const p of data.entries || []) {
      if (!byYear.has(p.year)) byYear.set(p.year, []);
      byYear.get(p.year).push(p);
    }

    const years = [...byYear.keys()].sort((a, b) => b - a);

    mount.innerHTML = years
      .map(
        (y) =>
          `<h3 class="pub-year">${y}</h3>` +
          byYear.get(y).map((p) => renderEntry(p, highlight)).join("")
      )
      .join("");
  }

  fetch("publications.json")
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then(render)
    .catch(() => {
      // fetch() fails on file:// URLs, so say something useful rather
      // than leaving "Loading..." on screen forever.
      mount.innerHTML =
        '<p class="loading">Could not load publications.json. ' +
        'If you are previewing locally, serve the folder over HTTP ' +
        '(<code>python3 -m http.server</code>) instead of opening the file directly. ' +
        'Meanwhile, see <a href="https://dblp.org/pid/163/3199">DBLP</a>.</p>';
    });
})();
