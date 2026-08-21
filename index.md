---
layout: single
author_profile: true
---

<section class="hero">
  <p class="hero-lede" style="margin-bottom:0.3em;">Postdoctoral researcher at QU Lab, TU Berlin & BIFOLD</p>
  <p class="hero-lede">
    I am a postdoc at the <a href="https://www.tu.berlin/qu">Quality and Usability Lab</a>,
    TU Berlin, affiliated with <a href="https://www.bifold.berlin/">BIFOLD</a> and the
    Speech and Language Technology group at <a href="https://www.dfki.de/en/web">DFKI Berlin</a>,
    as well as with <a href="https://ikim.charite.de/">Charité-IKIM, the Institute of Artificial Intelligence in Medicine.</a>
    I did my PhD jointly at TU Berlin and Université Paris-Saclay on cross-lingual
    information extraction for pharmacovigilance. <br>
    My work now focuses on robustness of language-based systems in the clinical/biomedical domain,
    anonymization techniques for clinical texts or texts written by patients and NLP-support for mental health.

    If you would like to talk, just drop me a line!

  </p>
</section>

<section id="research" markdown="1">

## <span class="tag">01</span> Research
{: #research-title}

<div class="themes">
  <article>
    <h3>Evaluation for clinical AI</h3>
    <p>
      A model that is fluent on a benchmark can still be unsafe in a ward. I am
      interested in counterfactual and adversarial evaluation designs that separate
      detecting a problem from localising it and from explaining it.
    </p>
  </article>

  <article>
    <h3>De-identification and re-identification risk</h3>
    <p>
      Removing names and dates is not the same as making a document safe. I study
      indirect identifiers, the quasi-identifying detail that survives standard
      de-identification, and how to measure the residual risk of a released corpus
      in a way that maps onto data protection law rather than onto token-level F1.
    </p>
  </article>

  <article>
    <h3>Multilingual pharmacovigilance</h3>
    <p>
      Adverse drug events are reported by patients in whatever language they speak,
      but detection systems are overwhelmingly English. I work on corpora and models
      that cover German, French, Japanese and beyond, and on what is missed when
      surveillance runs in English only.
    </p>
  </article>

  <article>
    <h3>Synthetic and shareable clinical corpora</h3>
    <p>
      Much clinical NLP is unreproducible because the data cannot travel. I contribute
      to open synthetic benchmarks and shared tasks so that methods can be compared
      without moving patient records.
    </p>
  </article>
</div>

</section>

<section id="publications" markdown="1">

## <span class="tag">02</span> Publications
{: #publications-title}

<p class="note">
  Most recent list on <a href="https://scholar.google.com/citations?user=S0TC4zMAAAAJ&hl=en">Google Scholar</a>.
</p>

{% assign entries = site.data.publications.entries %}
{% assign highlight = site.data.publications.highlight %}
{% assign year_groups = entries | group_by: "year" | sort: "name" | reverse %}
{% for grp in year_groups %}
<h3 class="pub-year">{{ grp.name }}</h3>
{% for p in grp.items %}
<div class="pub">
  <span class="pub-title">{{ p.title }}{% if p.kind %}<span class="kind">{{ p.kind }}</span>{% endif %}</span>
  <span class="pub-authors">{% for a in p.authors %}{% if a == highlight %}<span class="me">{{ a }}</span>{% else %}{{ a }}{% endif %}{% unless forloop.last %}{% if forloop.rindex == 2 %} and {% else %}, {% endif %}{% endunless %}{% endfor %}</span>
  <span class="pub-venue"><em>{{ p.venue }}</em></span>
  {% if p.links.size > 0 %}<span class="pub-links">{% for l in p.links %}<a href="{{ l.url }}">{{ l.label }}</a>{% endfor %}</span>{% endif %}
</div>
{% endfor %}
{% endfor %}

</section>

<section id="teaching" markdown="1">

## <span class="tag">03</span> Teaching &amp; service

### Supervision

I supervise B.Sc. and M.Sc. theses on clinical and biomedical NLP. Current topics
include anonymisation of therapeutic conversations, cross-lingual discourse analysis,
and health misinformation. If you are a student at TU Berlin and one of these sounds
like your kind of problem, write to me.

### Organisation

<ul class="plain">
  <li>
    <span class="tag">2026</span>
    Co-organiser, <a href="https://qulab.github.io/HeMAI2026/">HeMAI: Health and Multimodal AI</a>, workshop at ICMI 2026, Naples.
  </li>
  <li>
    <span class="tag">2026</span>
    Co-organiser together with Charlott Jakob, Workshop for <a href="https://lp4g.dfki.de/">"LLMs and Language Processing for Social Good"
  </li>
  <li>
    <span class="tag">2024, 2025, 2026</span>
    Co-organiser, SMM4H-HeaRD shared task on multilingual adverse drug event detection.
  </li>
</ul>

### Reviewing

ACL, EMNLP, NAACL, EACL, LREC-COLING, BioNLP, ClinicalNLP, Nature Communications, and related venues.

</section>

<section id="contact" markdown="1">

## <span class="tag">04</span> Contact
{: #contact-title}

<p><span class="tag">Email</span> last-name @ tu-berlin.de</p>

</section>
