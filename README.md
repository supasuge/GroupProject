# Manchester United and Soccer Culture in England

A small, deliberately simple, statically-rendered website built for an Oakland University class project on social movements and sports. The site explores soccer culture in England and the history of Manchester United.

The project is intentionally a four-page content site rather than an application. Content lives in Markdown files. A tiny custom Markdown converter renders those files into HTML using a single Jinja template. A short Flask app serves the same template locally for preview, and a separate script builds a static `dist/` folder that can be published directly to GitHub Pages.

---

## What each file does

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Original implementation specification (kept for reference). |
| `README.md` | This file. |
| `site_config.py` | Site metadata, page order, navigation labels, page descriptions. |
| `tiny_markdown.py` | Defensive, allow-listed Markdown → HTML converter. Returns rendered HTML, a list of headings (for the table of contents), and the page title extracted from the first `#` heading. |
| `app.py` | Flask preview server. Loads and parses every Markdown page once at startup; serves them via extensionless routes. |
| `build_static.py` | Static site builder. Wipes and rebuilds `dist/`, copies `static/` into it, and renders one HTML file per page using the same Jinja template Flask uses. |
| `templates/base.html` | Single page template, used by both `app.py` and `build_static.py`. |
| `static/mu.css` | All site styling — mobile-first, no JS, no frameworks. |
| `static/images/` | Local images. Every image used in the site must be cited in `content/sources.md`. |
| `content/*.md` | Source content for every page on the site. |
| `requirements.txt` | Python dependencies: Flask and MarkupSafe. |
| `Dockerfile` | Optional container that proves the static build runs cleanly on a pinned Ubuntu LTS. |
| `.github/workflows/pages.yml` | GitHub Actions workflow that builds and deploys `dist/` to GitHub Pages. |
| `.gitignore` | Ignores `dist/`, `.venv/`, caches, and OS junk. |

---

## Why the site is static-first

GitHub Pages serves static files, not a Flask application. The original spec described a request-rendered Flask site, which would not deploy as-is. The implementation here keeps Flask for local preview but treats `build_static.py` as the source of truth for what actually gets published: every output file under `dist/` is a self-contained HTML page that references CSS and images with simple top-level relative paths (`static/mu.css`, `static/images/...`). That keeps asset paths from breaking on project sites and avoids any need for a base-path config.

The same Jinja template is used by Flask and the static builder. The only difference between the two is the URL helper: Flask hands the template `page_url("home") → "/"` and `asset_url("mu.css") → "/static/mu.css"`; the static builder hands it `page_url("home") → "index.html"` and `asset_url("mu.css") → "static/mu.css"`.

---

## Setup

Create and activate a virtual environment, then install dependencies:

```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## Local Flask preview

```shell
python -m flask --app app run --debug
```

Then open <http://127.0.0.1:5000/>. Routes:

- `/` — home
- `/country-england` — Soccer in England
- `/team-manchester-united` — Manchester United history
- `/sources` — Sources

Unknown slugs return a 404 styled with the same chrome as the rest of the site.

---

## Building the static site

```shell
python build_static.py
```

Expected output:

```text
Built 4 pages into dist/
- index.html
- country-england.html
- team-manchester-united.html
- sources.html
```

The build script always deletes and recreates `dist/` before writing into it, so the output is never a mix of old and new files.

---

## Previewing the static build

```shell
python -m http.server 8000 -d dist
```

Then open <http://localhost:8000>. This is the closest local equivalent to what GitHub Pages will serve.

---

## Deploying to GitHub Pages

1. Push the repository to GitHub.
2. In the repository **Settings → Pages**, set the publishing source to **GitHub Actions**.
3. The `pages.yml` workflow runs automatically on every push to `main` (and can also be triggered manually). It installs dependencies, runs `build_static.py`, uploads `dist/` as a Pages artifact, and deploys it.

Do **not** commit the `dist/` folder. The workflow rebuilds it on every deploy and `.gitignore` already excludes it.

---

## Editing Markdown content

All page text lives in `content/*.md`. The filename (without `.md`) is the page slug. The order of pages, their navigation labels, and their meta descriptions are controlled in `site_config.py` — adding a new slug to `PAGE_ORDER` and creating a matching Markdown file is all that is needed to add a page.

Supported Markdown:

- `#`, `##`, `###` headings
- paragraphs
- `- ` unordered lists
- `**bold**` and `*italic*`
- `[link text](https://example.com)` links
- `![Alt text](static/images/foo.jpg)` images on their own line
- `>` blockquotes
- `---` horizontal rule

Raw HTML inside Markdown is **escaped** rather than passed through — see the limitations section below.

When you add a new section heading, the table of contents picks it up automatically. Stable, slugified heading IDs are generated from the heading text; duplicates get a `-2`, `-3`, … suffix.

---

## Adding images and citing them

1. Save the image into `static/images/`. Use lowercase, hyphenated filenames (`old-trafford-exterior.jpg`).
2. Embed it in Markdown with descriptive alt text:

   ```markdown
   ![Old Trafford exterior on a matchday](static/images/old-trafford-exterior.jpg)
   ```

3. Add an entry to the "Images and Media" section of `content/sources.md` with the filename, source URL or citation, photographer/owner, license, and the page on which it appears.

Image rules enforced by the Markdown converter:

- Image sources must start with `static/images/`.
- Paths containing `..` are rejected.
- `javascript:` and `data:` URLs are rejected.
- Every image is rendered with `loading="lazy"` and `decoding="async"`.
- Alt text becomes a visible `<figcaption>` as well, so captions and alt always stay in sync.

---

## Team responsibilities

- **Evan Pardon** — site scaffold, *Soccer in England* page, political landscape, economic structures, fan culture and traditions, media representation, draft/transfer milestones.
- **Jared Ekstrom** — historical development, founding and early history, legendary or influential players, stadium history and significance.
- **Lilliana Halliburton** — World Cup connections, fan base and supporter culture, political or social events connected to the team, contributions to national or global soccer culture, regional and ethnic identities.

---

## Known limitations of the tiny Markdown parser

The custom converter (`tiny_markdown.py`) intentionally implements only a small subset of Markdown. The trade-offs:

- **No raw HTML passthrough.** Anything that looks like HTML is escaped and displayed as text. This is a deliberate safety choice — never use `|safe` on the rendered output for anything other than the `RenderedMarkdown.html` value the converter itself produces.
- **No nested or ordered lists.** Only single-level unordered lists with `-` or `*` are supported.
- **No tables, no code fences, no images with title attributes.** Add a real Markdown library if you need these — keep in mind the security implications.
- **Inline images are treated as paragraphs.** Only an image *alone on its own line* becomes a `<figure>`.
- **Link URLs are restricted.** `javascript:`, `data:`, and `vbscript:` schemes are rejected; `..` is rejected; only `http://`, `https://`, `mailto:`, `#anchor`, or simple relative paths are allowed. External links automatically receive `target="_blank" rel="noopener noreferrer"`.

These limits are what keep the converter small, predictable, and safe to point at the open web.
