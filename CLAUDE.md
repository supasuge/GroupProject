# CLAUDE.md — Manchester United Soccer Culture Project Specification

## Mission

Build a polished, responsive, accessible content website for a class project about:

1. **Soccer in England**
2. **The history and cultural significance of Manchester United**

The original plan already chooses a deliberately simple architecture: Markdown content files, a tiny Markdown converter, Flask for local preview, static CSS, and no database/CMS/frontend framework. Preserve that simplicity, but improve the implementation into a production-ready class project that can be deployed to GitHub Pages as static HTML.

The final result should feel like a modern sports-history microsite: readable, image-friendly, visually connected to Manchester United colors, and easy for group members to edit through Markdown.

---

## Implementation Role

You are implementing this repository as a coding agent. Do not ask for clarification unless something is truly blocking. Make practical, minimal, high-quality decisions and document them in `README.md`.

Prioritize:

- correctness
- simple architecture
- readable code
- responsive design
- accessibility
- safe Markdown rendering
- easy GitHub Pages deployment
- clean content authoring workflow for classmates

---

## Non-Negotiable Constraints

- No database.
- No CMS.
- No React/Vue/Svelte/Angular or frontend framework.
- No CSS framework such as Bootstrap or Tailwind.
- Use Markdown files as the editable content source.
- Use Flask only for local preview/development.
- Generate static HTML into `dist/` for GitHub Pages deployment.
- Keep dependencies minimal: Flask, Jinja2 through Flask, MarkupSafe, and the Python standard library.
- Escape Markdown text before injecting generated HTML.
- Do not use `|safe` on raw/untrusted strings in templates.
- Do not hotlink random images. Store project images under `static/images/` and cite image sources in `content/sources.md`.
- Do not use Manchester United official crest/logo assets unless the project has permission or the asset is clearly allowed for the assignment. Prefer a text-based `MUFC` mark or abstract red/gold badge made with CSS.

---

## Recommended Architecture Adjustment

The source plan included Flask request rendering and GitHub Pages deployment. GitHub Pages serves static files, not a Flask app. Therefore, implement this as a **static-first site**:

- `app.py` previews the same pages locally with Flask.
- `build_static.py` renders Markdown + Jinja templates into static HTML in `dist/`.
- GitHub Pages publishes the generated `dist/` artifact.

Use top-level static output files to keep asset paths simple:

```text
dist/
├── index.html
├── country-england.html
├── team-manchester-united.html
├── sources.html
└── static/
    ├── mu.css
    └── images/
```

This avoids project-site base-path problems on GitHub Pages. All generated pages can reference CSS and images with paths such as:

```html
<link rel="stylesheet" href="static/mu.css">
<img src="static/images/old-trafford.jpg" alt="...">
```

For Flask preview, routes should be extensionless:

```text
/                       -> home
/country-england        -> Soccer in England
/team-manchester-united -> Manchester United history
/sources                -> Sources
```

For static output, links should be:

```text
index.html
country-england.html
team-manchester-united.html
sources.html
```

Inject a `page_url(slug)` helper into the template so Flask and static builds can use the same template without hardcoded routing logic.

---

## Final Deliverables

Create or update these files:

```text
manutd_site/
│
├── CLAUDE.md
├── README.md
├── requirements.txt
├── app.py
├── build_static.py
├── tiny_markdown.py
├── site_config.py
├── Dockerfile
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── pages.yml
│
├── content/
│   ├── home.md
│   ├── country-england.md
│   ├── team-manchester-united.md
│   └── sources.md
│
├── templates/
│   └── base.html
│
└── static/
    ├── mu.css
    └── images/
        └── .gitkeep
```

`dist/` is generated and should not be manually edited.

---

## Group Responsibilities To Preserve

Reflect these responsibilities in `README.md` and, if useful, on the homepage as a small “Project Team” section.

### Evan Pardon

- Create website scaffold.
- Soccer in England.
- Political Landscape.
- Economic Structures.
- Fan Culture and Traditions.
- Media Representation.
- Draft or Transfer Milestones.

### Jared Ekstrom

- Historical Development.
- Founding and Early History.
- Legendary or Influential Players.
- Stadium History and Significance.

### SavorySheikah

- World Cup Connections.
- Fan Base and Supporter Culture.
- Political or Social Events Connected to the Team.
- Contributions to National or Global Soccer Culture.
- Regional and Ethnic Identities.

---

## Content Requirements

### `content/home.md`

Purpose: landing page and project overview.

Required structure:

```markdown
# Manchester United and Soccer Culture in England

## Project Overview

## How to Use This Site

## Project Sections

## Team Responsibilities
```

The homepage should explain that the site is split into two major parts:

- country context: soccer in England
- team context: Manchester United history and culture

Keep homepage copy short and navigational. It should direct readers to the two main content pages and the sources page.

---

### `content/country-england.md`

Required structure:

```markdown
# Soccer in England

## Social and Cultural Life

## Historical Development

## Political Landscape

## Economic Structures

## Regional or Ethnic Identities

## Fan Culture and Traditions

## Media Representation
```

Each section should eventually include:

- 1–3 focused paragraphs
- clear connection to English soccer culture
- at least one source citation where factual claims are made
- optional local image using `static/images/...`

---

### `content/team-manchester-united.md`

Required structure:

```markdown
# History of Manchester United

## Founding and Early History

## Key or Pivotal Moments

## Legendary or Influential Players

## World Cup Connections

## Draft or Transfer Milestones

## Stadium History and Significance

## Fan Base and Supporter Culture

## Political or Social Events Connected to the Team

## Contributions to National or Global Soccer Culture
```

Notes:

- Soccer does not use an American-style draft system. The “Draft or Transfer Milestones” section should explain this clearly and focus on transfer milestones, youth development, and recruitment.
- For factual team history, prefer authoritative sources such as the club’s official history pages, Premier League records, FIFA, the FA, reputable museums, books, or high-quality journalism.
- Do not invent statistics, dates, transfer fees, or historical claims.

---

### `content/sources.md`

Required structure:

```markdown
# Sources

## Manchester United History

## English Soccer and Culture

## Stadium and Supporter Culture

## Images and Media
```

Every image used in the site must be listed here with:

- image filename
- source URL or citation
- photographer/owner if available
- license or usage note if available
- section/page where used

---

## Content Quality Standards

Each finished content section should answer:

1. What happened or what is the topic?
2. Why does it matter culturally, socially, politically, or economically?
3. How does it connect to England, Manchester United, or global soccer?
4. What source supports the claim?

Avoid weak filler such as:

- “Manchester United is a very important team.”
- “Fans are passionate.”
- “Soccer has many traditions.”

Prefer concrete writing:

- name the institution, event, player, stadium, competition, law, supporter group, media outlet, or social issue
- explain significance
- connect back to the class prompt

---

## Markdown Format Supported

The custom Markdown converter should stay intentionally small. Support only the syntax the project needs.

Required support:

```markdown
# H1
## H2
### H3

Paragraph text.

- unordered list item
- unordered list item

**bold text**
*italic text*

[link text](https://example.com)

![Alt text](static/images/example.jpg)

---
```

Optional but useful support:

```markdown
> blockquote text
```

Do not support raw HTML from Markdown. Raw HTML should be escaped and shown as text.

---

## Markdown Security Requirements

Implement `tiny_markdown.py` defensively.

### Inline Rules

- Escape text first with `markupsafe.escape`.
- Then apply the small allowlist of Markdown transformations.
- Only generate known-safe tags:
  - `h1`, `h2`, `h3`
  - `p`
  - `ul`, `li`
  - `strong`, `em`
  - `a`
  - `figure`, `img`, `figcaption`
  - `blockquote`
  - `hr`
- Links must allow only:
  - `https://...`
  - `http://...` only if there is a reason, but prefer HTTPS
- External links must include:

```html
target="_blank" rel="noopener noreferrer"
```

### Image Rules

For Markdown images:

```markdown
![Old Trafford exterior](static/images/old-trafford.jpg)
```

Generate:

```html
<figure class="content-figure">
  <img src="static/images/old-trafford.jpg" alt="Old Trafford exterior" loading="lazy" decoding="async">
</figure>
```

Rules:

- `alt` is required; if empty, render a warning comment in development or use a descriptive fallback.
- Local images must live under `static/images/`.
- Do not allow arbitrary file paths such as `../secret.txt`.
- Do not allow `javascript:` or data URLs.

### Headings and Table of Contents

Generate stable IDs for `h2` and `h3` headings.

Example:

```markdown
## Stadium History and Significance
```

Should become:

```html
<h2 id="stadium-history-and-significance">Stadium History and Significance</h2>
```

Also collect sections for an on-page table of contents:

```python
{
    "id": "stadium-history-and-significance",
    "title": "Stadium History and Significance",
    "level": 2,
}
```

If duplicate headings occur, append `-2`, `-3`, etc.

---

## Python Design Requirements

Use Python 3.12+ style code.

### `site_config.py`

Centralize page ordering and site metadata.

Required constants:

```python
SITE_TITLE = "Manchester United Project"
SITE_DESCRIPTION = "A class project exploring soccer culture in England and the history of Manchester United."
CONTENT_DIR = "content"
STATIC_DIR = "static"
DIST_DIR = "dist"

PAGE_ORDER = [
    "home",
    "country-england",
    "team-manchester-united",
    "sources",
]
```

Also include display labels only if needed. Prefer extracting titles from Markdown `#` headings.

---

### `tiny_markdown.py`

Recommended public API:

```python
from dataclasses import dataclass
from markupsafe import Markup

@dataclass(frozen=True)
class Section:
    id: str
    title: str
    level: int

@dataclass(frozen=True)
class RenderedMarkdown:
    html: Markup
    sections: list[Section]

class TinyMarkdown:
    def convert(self, markdown: str) -> RenderedMarkdown:
        ...
```

This allows templates to render a table of contents without reparsing Markdown.

---

### `app.py`

Purpose: local preview only.

Requirements:

- Load all Markdown pages at startup.
- Parse Markdown once into cached page objects.
- Do not read Markdown on every request.
- Use `abort(404)` for unknown slugs.
- Inject `page_url` helper for Flask routes.
- Set active navigation state with `aria-current="page"`.

Routes:

```python
@app.get("/")
def home():
    ...

@app.get("/<slug>")
def show_page(slug: str):
    ...
```

`home` should internally render the `home` slug.

---

### `build_static.py`

Purpose: production build for GitHub Pages.

Requirements:

- Delete and recreate `dist/` on each build.
- Copy `static/` into `dist/static/`.
- Render each Markdown page to an HTML file:
  - `home` -> `dist/index.html`
  - all other slugs -> `dist/<slug>.html`
- Use the same Jinja template as Flask.
- Inject a static `page_url(slug)` helper:
  - `home` -> `index.html`
  - other pages -> `<slug>.html`
- Fail loudly if a required content file is missing.
- Print a build summary listing generated pages.

Expected command:

```shell
python build_static.py
```

Expected output example:

```text
Built 4 pages into dist/
- index.html
- country-england.html
- team-manchester-united.html
- sources.html
```

---

## Template Requirements

### `templates/base.html`

Use semantic HTML and accessible landmarks.

Required structure:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ page.title }} | {{ site_title }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{{ page.description or site_description }}">
  <link rel="stylesheet" href="{{ asset_url('mu.css') }}">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>

  <header class="site-header">
    <nav class="nav container" aria-label="Primary navigation">
      <a class="brand" href="{{ page_url('home') }}" aria-label="Manchester United Project home">
        <span class="brand-mark" aria-hidden="true">MU</span>
        <span class="brand-text">MUFC Project</span>
      </a>

      <div class="nav-links">
        {% for slug, item in pages.items() %}
          <a href="{{ page_url(slug) }}" {% if slug == page.slug %}aria-current="page"{% endif %}>
            {{ item.title }}
          </a>
        {% endfor %}
      </div>
    </nav>
  </header>

  <main id="main-content" class="site-main">
    <section class="hero container" aria-labelledby="page-title">
      <div class="hero-copy">
        <p class="eyebrow">Soccer Culture Project</p>
        <h1 id="page-title">{{ page.title }}</h1>
        {% if page.description %}
          <p class="hero-lede">{{ page.description }}</p>
        {% endif %}
      </div>
      <div class="hero-card" aria-label="Project focus">
        <span>England</span>
        <strong>Manchester United</strong>
        <span>History • Culture • Supporters</span>
      </div>
    </section>

    <div class="content-layout container">
      <article class="page-card">
        {{ page.body_html }}
      </article>

      {% if page.sections %}
        <aside class="toc" aria-labelledby="toc-heading">
          <h2 id="toc-heading">On this page</h2>
          <ol>
            {% for section in page.sections %}
              <li class="toc-level-{{ section.level }}">
                <a href="#{{ section.id }}">{{ section.title }}</a>
              </li>
            {% endfor %}
          </ol>
        </aside>
      {% endif %}
    </div>
  </main>

  <footer class="footer">
    <div class="container footer-inner">
      <p>Soccer Culture Project — Manchester United Theme</p>
      <a href="{{ page_url('sources') }}">Sources</a>
    </div>
  </footer>
</body>
</html>
```

Adjust exact markup as needed, but keep these concepts:

- skip link
- semantic header/nav/main/article/aside/footer
- active nav state
- responsive hero
- readable article card
- optional table of contents
- source link in footer

---

## UI/UX Direction

### Visual Concept

Blend two moods:

1. **Matchday energy**: red, gold, black, bold header, strong visual rhythm.
2. **Museum/history readability**: clean cards, strong headings, generous line length, image captions, source-friendly layout.

The site should not look like a raw school handout. It should look like a finished, curated web exhibit.

---

## Styling Requirements

### `static/mu.css`

Use a mobile-first stylesheet with CSS custom properties.

Start with these tokens and refine only if contrast remains strong:

```css
:root {
  --mu-red: #c70101;
  --mu-red-dark: #730000;
  --mu-red-deep: #3b0505;
  --mu-gold: #f5c542;
  --mu-gold-soft: #ffe08a;
  --mu-black: #0d0d0f;
  --mu-ink: #111114;
  --mu-surface: #18181b;
  --mu-surface-2: #232326;
  --mu-border: rgba(255, 255, 255, 0.14);
  --mu-text: #f8f8f8;
  --mu-muted: #d7d7dc;
  --mu-subtle: #a7a7ad;
  --focus-ring: #ffe08a;

  --font-sans: Arial, Helvetica, sans-serif;
  --container: 1120px;
  --radius-lg: 24px;
  --radius-md: 16px;
  --shadow-soft: 0 24px 70px rgba(0, 0, 0, 0.35);
  --shadow-red: 0 0 42px rgba(199, 1, 1, 0.25);
}
```

### Base Layout

Required behavior:

```css
* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  min-height: 100vh;
  font-family: var(--font-sans);
  color: var(--mu-text);
  background:
    radial-gradient(circle at top left, rgba(199, 1, 1, 0.28), transparent 34rem),
    linear-gradient(135deg, var(--mu-black), #171717 55%, var(--mu-red-deep));
  line-height: 1.65;
}

.container {
  width: min(100% - 2rem, var(--container));
  margin-inline: auto;
}
```

Use fluid type:

```css
h1 {
  font-size: clamp(2.1rem, 6vw, 4.75rem);
  line-height: 0.98;
}

h2 {
  font-size: clamp(1.45rem, 3vw, 2.2rem);
}

p,
li {
  font-size: clamp(1rem, 1.5vw, 1.08rem);
}
```

### Header and Navigation

Requirements:

- sticky header
- strong red-to-dark gradient
- gold bottom accent
- brand mark created with CSS/text, not image logo
- responsive nav that wraps or horizontally scrolls on small screens
- no hamburger menu required
- links must have hover and focus-visible states
- active page must be visually distinct

Mobile behavior:

- brand on first line if needed
- nav links become pill-like horizontal scroll row
- touch targets should be at least 44px tall
- no text should overflow the viewport

### Hero Section

Requirements:

- large page title
- short eyebrow label
- optional description
- decorative project-focus card
- responsive two-column layout on desktop
- single-column layout under roughly `760px`

Suggested desktop layout:

```css
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(16rem, 0.6fr);
  gap: clamp(1.25rem, 4vw, 3rem);
  align-items: stretch;
  padding-block: clamp(2rem, 6vw, 5rem);
}
```

### Main Content Layout

Desktop:

- article card on the left
- sticky table of contents on the right

Mobile/tablet:

- single column
- table of contents moves above or below article
- no sticky behavior on narrow screens

Suggested:

```css
.content-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 17rem;
  gap: clamp(1.25rem, 4vw, 2rem);
  align-items: start;
}

@media (max-width: 960px) {
  .content-layout {
    grid-template-columns: 1fr;
  }

  .toc {
    position: static;
    order: -1;
  }
}
```

### Article Card

Requirements:

- readable line length
- high contrast
- soft border
- red/gold accenting
- section separation
- good spacing after headings

Suggested:

```css
.page-card {
  background: rgba(24, 24, 27, 0.92);
  border: 1px solid var(--mu-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-soft), var(--shadow-red);
  padding: clamp(1.25rem, 4vw, 3rem);
}

.page-card > * {
  max-width: 72ch;
}
```

### Headings

Requirements:

- `h1` appears in hero, not duplicated awkwardly inside card if possible
- `h2` should be visually scannable with a red left border or gold underline
- `h3` should be gold or muted gold
- heading IDs should support anchor links

### Links

Requirements:

- gold link color
- underline offset
- visible focus state
- external link safe attributes

Suggested:

```css
a {
  color: var(--mu-gold-soft);
  text-underline-offset: 0.18em;
}

a:hover {
  color: #fff2bf;
}

:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 4px;
}
```

### Cards and Lists

Improve raw lists so they feel intentional:

- list items have breathing room
- bullets can use gold accent through `::marker`
- optional cards for homepage project sections and team responsibilities

```css
li::marker {
  color: var(--mu-gold);
}
```

### Images and Figures

Requirements:

- responsive images
- rounded corners
- captions
- lazy loading from converter
- visible source/credit nearby when necessary

Suggested:

```css
.content-figure {
  max-width: 100%;
  margin: 2rem 0;
}

.content-figure img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: var(--radius-md);
  border: 1px solid var(--mu-border);
}

.content-figure figcaption {
  margin-top: 0.65rem;
  color: var(--mu-subtle);
  font-size: 0.95rem;
}
```

### Table of Contents

Requirements:

- sticky on desktop
- card style
- compact but readable
- highlights hover/focus
- hides `h1`; includes `h2` and optionally `h3`
- line height and indentation distinguish heading levels

### Footer

Requirements:

- simple footer
- link to sources
- match theme
- no clutter

---

## Responsive Design Requirements

Design mobile-first and verify these viewport widths:

- 360px: small phones
- 390px: common modern phones
- 768px: tablet portrait
- 1024px: tablet/desktop boundary
- 1280px+: desktop

Acceptance rules:

- No horizontal scrolling on the body.
- Nav remains usable at 360px width.
- Cards do not create cramped gutters on mobile.
- Article text remains readable without zooming.
- Images shrink fluidly.
- Touch targets are comfortable.
- Sticky table of contents is disabled on narrow screens.
- `h1` does not overflow on mobile.

Use these breakpoint guidelines:

```css
@media (max-width: 760px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .nav {
    align-items: flex-start;
  }

  .nav-links {
    width: 100%;
    overflow-x: auto;
    padding-bottom: 0.25rem;
  }
}

@media (max-width: 520px) {
  .container {
    width: min(100% - 1rem, var(--container));
  }

  .page-card,
  .toc,
  .hero-card {
    border-radius: 18px;
  }
}
```

---

## Accessibility Requirements

Implement the following:

- `<html lang="en">`
- skip link to main content
- semantic landmarks
- one visible page-level `h1`
- proper heading order
- descriptive link text
- `aria-current="page"` for active navigation
- keyboard-visible focus states
- sufficient color contrast
- images require descriptive alt text
- decorative text/visual marks use `aria-hidden="true"`
- do not communicate meaning by color alone
- respect reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Performance Requirements

- No heavy client-side JavaScript.
- No external font requests.
- Use system fonts.
- Optimize images before committing.
- Use `loading="lazy"` and `decoding="async"` for Markdown-rendered images.
- Keep CSS in one file: `static/mu.css`.
- Static build should complete quickly and deterministically.

---

## GitHub Pages Deployment

Create `.github/workflows/pages.yml`.

Use GitHub Pages Actions deployment with `dist/` as the artifact path.

Required workflow shape:

```yaml
name: Deploy static site to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: python -m pip install --upgrade pip && python -m pip install -r requirements.txt

      - name: Build static site
        run: python build_static.py

      - name: Upload GitHub Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

In `README.md`, tell users to enable GitHub Pages with source set to **GitHub Actions**.

---

## Dockerfile Requirements

The original plan asked for an Ubuntu Dockerfile. Use a pinned Ubuntu LTS image instead of `ubuntu:latest` for reproducibility.

Recommended `Dockerfile`:

```Dockerfile
FROM ubuntu:24.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip \
    && /opt/venv/bin/python -m pip install -r requirements.txt

COPY . .
RUN /opt/venv/bin/python build_static.py

FROM ubuntu:24.04 AS static-artifact
WORKDIR /site
COPY --from=builder /app/dist ./dist
```

This proves the static build works inside Ubuntu. Do not use Docker as the primary GitHub Pages deployment mechanism; GitHub Actions should run `build_static.py` directly.

---

## README.md Requirements

`README.md` must include:

1. Project summary.
2. What each file does.
3. Why the site is static-first.
4. How to create a virtual environment.
5. How to run local Flask preview.
6. How to build static output.
7. How to preview `dist/` locally.
8. How to deploy to GitHub Pages.
9. How group members should edit Markdown content.
10. How to add images and cite them.
11. Team responsibilities.
12. Known limitations of the tiny Markdown parser.

Required commands:

```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app app run --debug
```

Static build:

```shell
python build_static.py
python -m http.server 8000 -d dist
```

Then open:

```text
http://localhost:8000
```

Windows PowerShell activation note:

```powershell
.venv\Scripts\Activate.ps1
```

---

## `requirements.txt`

Keep minimal:

```text
Flask>=3.0,<4.0
MarkupSafe>=3.0,<4.0
```

Do not add Markdown libraries unless explicitly changing the assignment design. The point of this implementation is to use the small custom converter.

---

## `.gitignore`

Required entries:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.dist/
dist/
.DS_Store
.env
```

Do not commit generated `dist/` unless the instructor specifically wants static output committed.

---

## Testing and Verification

Before finishing, run these checks:

```shell
python -m compileall .
python build_static.py
python -m flask --app app run --debug
python -m http.server 8000 -d dist
```

Manual browser checks:

- home page loads
- each nav link works in Flask preview
- each nav link works in `dist/` preview
- CSS loads in Flask preview
- CSS loads in `dist/` preview
- table of contents anchors jump to sections
- mobile layout works at 360px width
- keyboard tab navigation is visible
- unknown Flask route returns 404

Optional lightweight tests if time permits:

- Markdown headings render correctly.
- unsafe HTML is escaped.
- links render with safe external attributes.
- duplicate heading IDs are unique.
- static builder creates exactly the expected HTML files.

---

## Acceptance Criteria

The project is complete when:

- `python build_static.py` creates a valid `dist/` folder.
- `dist/index.html` loads with full styling.
- `dist/country-england.html`, `dist/team-manchester-united.html`, and `dist/sources.html` exist.
- Local Flask preview works.
- GitHub Pages workflow is present and uses `dist/`.
- Site has responsive layout for mobile/tablet/desktop.
- The nav is accessible and usable without JavaScript.
- Markdown content renders safely through the custom converter.
- The pages include the required assignment section headings.
- Styling is meaningfully improved beyond the original simple CSS.
- README explains setup, editing, static build, and deployment.

---

## Design Polish Checklist

Use this as the final pass:

- [ ] The homepage feels intentional, not just text dumped onto a page.
- [ ] The red/gold theme is visible but not overwhelming.
- [ ] Body copy has a comfortable line length.
- [ ] Headings create a clear hierarchy.
- [ ] Cards and spacing are consistent.
- [ ] Mobile nav is usable.
- [ ] Focus states are visible.
- [ ] Images have rounded corners, alt text, and citations.
- [ ] Sources page is easy to scan.
- [ ] No horizontal overflow.
- [ ] No raw HTML injection from Markdown.
- [ ] No unnecessary dependencies.

---

## Common Mistakes To Avoid

- Building only a Flask app and calling it GitHub Pages-ready.
- Using `ubuntu:latest` instead of a pinned version.
- Adding a frontend framework for a four-page content site.
- Re-parsing Markdown on every request.
- Using `|safe` on untrusted Markdown text.
- Letting mobile nav overflow off-screen.
- Making red body text on a black background.
- Using copyrighted logos or random hotlinked images without attribution.
- Inventing Manchester United historical claims without sources.
- Forgetting that soccer transfer systems are not drafts.
- Committing `dist/` accidentally if the workflow builds it.

---

## Implementation Order

Follow this order:

1. Create/clean project structure.
2. Add `site_config.py`.
3. Implement `tiny_markdown.py` with safe rendering and heading IDs.
4. Add Markdown content stubs with required headings.
5. Build `templates/base.html` with semantic layout and URL helpers.
6. Implement `app.py` local preview and page cache.
7. Implement `build_static.py` static renderer.
8. Write improved `static/mu.css`.
9. Add `requirements.txt`, `.gitignore`, `Dockerfile`, and GitHub Pages workflow.
10. Write `README.md`.
11. Run build and preview checks.
12. Fix responsive and accessibility issues.

---

## Official Reference Links For Implementer

Use official docs when confirming deployment and framework behavior:

- GitHub Pages publishing source and Actions deployment: `https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site`
- GitHub Pages custom workflows: `https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages`
- Flask quickstart: `https://flask.palletsprojects.com/en/stable/quickstart/`
- MarkupSafe escaping: `https://markupsafe.palletsprojects.com/en/stable/escaping/`

---

## Final Quality Bar

The finished site should look like a small but complete digital exhibit, not a code demo. The implementation should remain simple enough that classmates can edit Markdown confidently, but polished enough that the final presentation feels deliberate, responsive, and credible.
