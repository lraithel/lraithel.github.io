---
layout: single
author_profile: true
---

<section class="hero">
  <h1 class="hero-tagline">Postdoctoral researcher at QU Lab, TU Berlin &amp; BIFOLD</h1>
  <p class="hero-lede">
    I am a postdoc at the <a href="https://www.tu.berlin/qu">Quality and Usability Lab</a>,
    TU Berlin, affiliated with <a href="https://www.bifold.berlin/">BIFOLD</a> and the
    Speech and Language Technology group at <a href="https://www.dfki.de/en/web">DFKI Berlin</a>,
    as well as with <a href="https://ikim.charite.de/">Charité-IKIM, the Institute of Artificial Intelligence in Medicine.</a>
    I did my PhD jointly at TU Berlin and Université Paris-Saclay on cross-lingual
    information extraction for pharmacovigilance. <br>
    My work now focuses on robustness of language-based systems in the clinical/biomedical domain,
    anonymization techniques for clinical texts or texts written by patients and NLP-support for mental health.<br>

    If you would like to talk, just drop me a line!
    You can also check out the <a href="https://www.tu.berlin/en/qu/research/research-groups/health-legal-language-technology">lab's</a> website.

  </p>
</section>

<section id="research" markdown="1">

## <span class="tag">01</span> Research
{: #research-title}

<div class="themes">
  <article>
    <h3>Evaluation for clinical AI</h3>
    <p>
      Getting the right label on a benchmark is not the same as being safe to use on a real patient. I work on counterfactual and adversarial evaluation designs to check whether a model actually catches a problem, can point to where it is, and can explain why - three different questions that a single accuracy number tends to hide.
    </p>
  </article>

  <article>
    <h3>De-identification and re-identification risk</h3>
    <p>
      I look at indirect identifiers - the details left in a document after names and dates are removed that can still narrow a patient down, like a rare diagnosis or an unusual age and location combination. Under HIPAA that risk is supposed to be measured, not assumed, and I work on ways to actually quantify how much of it survives standard de-identification.
    </p>
  </article>

  <article>
    <h3>Multilingual pharmacovigilance</h3>
    <p>
      Patients report side effects in whatever language they speak, but almost all detection systems are trained and tested in English. I build corpora and models for German, French, and Japanese, and try to figure out what gets missed when surveillance only runs in one language.
    </p>
  </article>

  <article>
    <h3>Synthetic and shareable clinical corpora</h3>
    <p>
      A lot of clinical NLP results can't be reproduced simply because the data behind them can never leave the hospital. I work on synthetic benchmarks and shared tasks that let people compare methods against each other without ever moving a real patient record.
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

{% assign entries = site.data.publications.entries | where_exp: "e", "e.kind != 'preprint'" %}
{% assign highlight = site.data.publications.highlight %}
{% assign year_groups = entries | group_by: "year" | sort: "name" | reverse %}
{% for grp in year_groups %}
<details class="pub-year-group"{% if forloop.first %} open{% endif %}>
  <summary class="pub-year">{{ grp.name }} <span class="pub-count">({{ grp.items.size }})</span></summary>
  <div class="pub-year-body">
  {% for p in grp.items %}
  <div class="pub">
    <span class="pub-title">{{ p.title }}{% if p.kind %}<span class="kind">{{ p.kind }}</span>{% endif %}</span>
    <span class="pub-authors">{% for a in p.authors %}{% if a == highlight %}<span class="me">{{ a }}</span>{% else %}{{ a }}{% endif %}{% if p.equal_contrib_count and forloop.index <= p.equal_contrib_count %}<sup>*</sup>{% endif %}{% unless forloop.last %}{% if forloop.rindex == 2 %} and {% else %}, {% endif %}{% endunless %}{% endfor %}</span>
    <span class="pub-venue"><em>{{ p.venue }}</em></span>
    {% if p.links.size > 0 %}<span class="pub-links">{% for l in p.links %}<a href="{{ l.url }}">{{ l.label }}</a>{% endfor %}</span>{% endif %}
  </div>
  {% endfor %}
  </div>
</details>
{% endfor %}

<p class="note">* Equal contribution.</p>

</section>

<section id="teaching" markdown="1">

## <span class="tag">03</span> Teaching &amp; service

### Supervision

I supervise B.Sc. and M.Sc. theses on clinical and biomedical NLP. Current topics include anonymisation of therapeutic conversations, cross-lingual discourse analysis, and health misinformation. If you are a student at TU Berlin or Potsdam University and one of these sounds like your kind of problem, write to me.

### Organisation

<ul class="plain">
  <li>
    <span class="tag">2026</span>
    Co-organiser, <a href="https://qulab.github.io/HeMAI2026/">HeMAI: Health and Multimodal AI</a>, workshop at ICMI 2026, Naples.
  </li>
  <li>
    <span class="tag">2026</span>
    Co-organiser, with Charlott Jakob, of the workshop <a href="https://lp4g.dfki.de/">"LLMs and Language Processing for Social Good"</a>.
  </li>
  <li>
    <span class="tag">2024, 2025, 2026</span>
    Co-organiser, <a href="https://healthlanguageprocessing.org/smm4h-2026/">SMM4H-HeaRD</a> shared task on multilingual adverse drug event detection.
  </li>
</ul>

### Reviewing

ACL, EMNLP, NAACL, EACL, LREC, COLING, BioNLP, ClinicalNLP, Nature Communications, and related venues/journals.

</section>

<section id="freelancing" markdown="1">

## <span class="tag">04</span> Freelancing
{: #freelancing-title}

Alongside my research, I sometimes take on freelance and advisory work at
the intersection of NLP and healthcare (and sometimes other topics such as
deepfake detection). Bridging the gap between academia and industry is
exciting, and often provides a different perspective on problems we try to
solve with AI.

<ul class="plain">
  <li>
    <span class="tag">Advisory</span>
    Scientific advisory for health-tech and NLP products, e.g. ongoing work with <a href="https://gretchen-ai.com/de/">Gretchen AI</a>.
  </li>
  <li>
    <span class="tag">Talks</span>
    Invited talks and workshops on clinical NLP, multilingual pharmacovigilance, and de-identification.
  </li>
</ul>

Interested in working together? Get in touch via the <a href="#contact">contact section below</a>.

</section>

<section id="contact" markdown="1">

## <span class="tag">05</span> Contact
{: #contact-title}

<p><span class="tag">Email</span> last name @ tu-berlin.de</p>

</section>
