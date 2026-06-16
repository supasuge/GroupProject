# Content Curation Report

Working log of changes made while curating **Sports Essay Dumping Ground.docx** (the group's
shared working document) into the live site. Each phase below was implemented and verified
individually before moving to the next. Nothing in this effort has been committed yet — all
changes sit in the working tree for group review.

> Status as of this report: **all phases complete, build verified.**

---

## Phase 0 — Source extraction (findings)

The uploaded `.docx` is a 22 MB Office Open XML package. It was unzipped to a scratch
directory and parsed directly from `word/document.xml` (plus `word/_rels/document.xml.rels`)
so that text paragraphs and embedded images could be recovered **in true reading order** and
each image associated with the section it sits next to.

Findings:

- **17 embedded images** (`word/media/image1.png` … `image17.png`), all PNG.
- The document is a "dumping ground": raw, pre-merge drafts from group members, separated by
  horizontal rules, with author tags (Lillian Halliburton, Evan Pardon, and an untagged
  Manchester United history section).
- One inline editorial note — *"maybe don't need to include this picture"* — appears
  immediately after `image6.png` (a 1920s squad photo). Treated as an author instruction to
  exclude that image from the live pages.
- The draft contains a few factual slips that conflict with the already-published, sourced
  pages (e.g. Munich casualty counts of "22 / 7 players" vs. the established 23 dead / 8
  players). **The accurate published figures were kept**; the draft's lower numbers were not
  imported.
- Two academic citations were referenced in-text but not yet in the project's citation
  module: `(Bandura et al, 2023)` and `(Armstrong, 1998)`, plus a Wikipedia URL.

Image → section map recovered from document order:

| Document order | File | Section it accompanies |
|---|---|---|
| 1–2 | image17, image10 | Club Formation / Founding |
| 3–4 | image12, image4 | Early Years |
| 5 | image2 | Old Trafford built (1909) |
| 6 | image11 | World War One |
| 7 | image6 | After the War (1920s) — *flagged "maybe don't need"* |
| 8–9 | image7, image9 | World War Two / Busby arrives |
| 10–11 | image16, image1 | Busby Babes |
| 12 | image5 | Munich air disaster (1958) |
| 13–16 | image13, image8, image15, image14 | 1968 European Cup era |
| 17 | image3 | Soccer in England (Evan's section) |

---

## Phase 1 — Image staging & optimization (changes)

All 17 images were copied into `static/images/` with descriptive, hyphenated names, downscaled
to a 1600 px max dimension (only ever shrinking, never upscaling), metadata stripped, and then
compressed with `pngquant` (quality 65–90).

- **Total weight: 12 MB → 6.3 MB.**
- Two academic-source citations were verified with web search before being trusted:
  - Bandura et al. (2023), *Drugs: Education, Prevention and Policy*, DOI `10.1080/09687637.2023.2219370`.
  - Gary Armstrong, *Football Hooligans: Knowing the Score* (Berg, 1998).

Filename mapping (original → site):

| Original | Site filename |
|---|---|
| image17 | `newton-heath-crest.png` |
| image10 | `newton-heath-team.png` |
| image12 | `early-united-squad.png` |
| image4  | `railway-station-homecoming.png` |
| image2  | `old-trafford-aerial-early.png` |
| image11 | `united-squad-ww1-era.png` |
| image6  | `united-squad-1920s.png` *(staged but not embedded)* |
| image7  | `old-trafford-bombed-1941.png` |
| image9  | `matt-busby.png` |
| image16 | `busby-babes-player.png` |
| image1  | `busby-babes-lineup.png` |
| image5  | `munich-air-disaster-1958.png` |
| image13 | `european-cup-squad-1968.png` |
| image8  | `players-celebrate-dressing-room-1968.png` |
| image15 | `albert-square-homecoming-1968.png` |
| image14 | `european-cup-parade-1968.png` |
| image3  | `english-football-modern-match.png` |

A convenience archive, **`manutd-site-images.zip`**, was written at the project root containing
the full `images/` set. (It is an untracked deliverable, not required by the build.)

---

## Phase 2 — Content curation (changes)

The existing pages already held polished, sourced prose, so the curation **preserved that prose
and integrated the document's images plus a few concrete facts**, rather than replacing good
writing with the rougher draft.

### `content/team-manchester-united.md` — 15 figures added

Images placed into the required section headings (kept per `CLAUDE.md`):

- **Founding and Early History** — crest, Newton Heath team, early United squad.
- **Key or Pivotal Moments** — Busby Babes lineup, Munich wreckage, 1968 squad.
- **Legendary or Influential Players** — Babes-era player, Sir Matt Busby, 1968 celebration.
- **Stadium History and Significance** — early Old Trafford aerial, 1941 bombing.
- **Fan Base and Supporter Culture** — railway homecoming, Albert Square 1968, 1968 bus parade.
- **Political or Social Events Connected to the Team** — wartime (WWI-era) squad.

Factual details woven in from the document (all consistent with established history):

- Newton Heath's alternate proposed names — *Manchester Central* and *Manchester Celtic*.
- Winger **Billy Meredith** ("the Welsh Wizard") as a catalyst for the 1908/1909 successes.
- **James Gibson**'s 1931 rescue of the club from near-bankruptcy.
- The **1915 match-fixing scandal** and **Sandy Turnbull**'s death in France in 1917 (new
  opening paragraph for the Political/Social section).

### `content/country-england.md` — 1 figure added

- **Social and Cultural Life** — modern-match crowd image, plus a sourced sentence on England
  registering 40,000+ clubs and hosting the world's oldest knockout competition (the FA Cup).

### Markdown converter constraint honored

`tiny_markdown.py` generates the `<figcaption>` from the image **alt text**, so every alt was
written to double as a descriptive, accurate caption. Identities that could not be verified
from the image alone were described cautiously (e.g. "a Busby Babes–era player") rather than
named.

---

## Phase 3 — Citation module expansion (changes)

`academic_citations.py` grew from **8 → 26** sources. Added:

- **From the document:** `bandura2023` (journal), `armstrong1998` (book),
  `wikipedia_football_england` (webpage).
- **Every `content/sources.md` entry not already represented in the module:**
  official Manchester United history, Premier League history, UEFA history, BBC Charlton
  obituary, Guardian archive, The FA, EFL, House of Commons Library regulator briefing,
  Kick It Out, Hillsborough Independent Panel, Inglis (*Engineering Archie*), MUST,
  FC United of Manchester, BBC Rashford timeline, Sport Scroll.

`uv run python academic_citations.py` runs clean and prints all 26 formatted references. As the
module's own docstring notes, the generated APA strings should still get a human proofreading
pass before final submission (a couple of organization-author entries render a cosmetic double
period — a pre-existing formatting behavior, not introduced here).

---

## Phase 4 — Source documentation (changes)

`content/sources.md`:

- Added Bandura (2023), Armstrong (1998), and the Wikipedia reference under
  *English Soccer and Culture*, keeping the page in sync with the citation module.
- Rewrote the **Images and Media** section from a placeholder into a full per-image credit
  list, grouped by page, naming every embedded file and the section it appears in, and listing
  the one staged-but-unused image.

**Honest provenance caveat recorded in `sources.md`:** these are archival photographs compiled
in the group's working document. Original photographers/rights-holders are **not yet
confirmed**, so licensing must be verified before any public deployment. They are reproduced
for a non-commercial class exhibit.

---

## Phase 5 — Build & verification (results)

```
uv run python -m compileall …        → compile OK
uv run python build_static.py        → Built 4 pages into dist/
```

Checks performed on the generated `dist/`:

- **17 images** copied into `dist/static/images/`.
- **16 figures** rendered: 15 on the Manchester United page, 1 on the England page.
- **0 missing image references** (every `static/images/*.png` referenced in HTML exists on disk).
- **0 unsafe-path fallbacks** (no literal `![…]` leaked into the HTML, i.e. every image passed
  the converter's `static/images/` allow-list).
- Headless-Chrome screenshots at **1280 px** and **390 px** confirm figures sit inside the
  article cards with captions and reflow correctly on mobile — no horizontal overflow.

---

## Files touched

| File | Change |
|---|---|
| `static/images/*.png` (17 new) | Extracted, renamed, optimized image set. |
| `content/team-manchester-united.md` | 15 figures + factual additions. |
| `content/country-england.md` | 1 figure + sourced detail. |
| `content/sources.md` | New academic sources + full image credits. |
| `academic_citations.py` | +18 source entries (8 → 26). |
| `manutd-site-images.zip` | Downloadable image bundle (untracked, optional). |
| `REPORT.md` | This log. |
| `README.md` | Updated for the new image set, citation module, and contributor name. |

> Note: `templates/base.html` also shows as modified, but that is from the **preceding**
> session (favicon + hero "focus card" overlap fix), not this content-curation work.

---

## Open items for the group

1. **Verify image licensing** before the site is made public — provenance is unconfirmed.
2. **Proofread the generated APA references** (`uv run python academic_citations.py`).
3. Decide whether to commit the new images and the `.docx` source, and whether to keep
   `manutd-site-images.zip` in the repo or treat it as a one-off deliverable.
