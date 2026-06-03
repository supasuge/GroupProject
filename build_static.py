"""Render the Markdown content into static HTML for GitHub Pages.

This script wipes ``dist/`` and rebuilds it from scratch every run so the
output is always a clean reflection of the current content. The same
Jinja template used by ``app.py`` is reused here; only the ``page_url``
and ``asset_url`` helpers change to produce relative paths that work
when published to GitHub Pages.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

import site_config
from tiny_markdown import RenderedMarkdown, TinyMarkdown


ROOT = Path(__file__).resolve().parent
CONTENT_ROOT = ROOT / site_config.CONTENT_DIR
STATIC_ROOT = ROOT / site_config.STATIC_DIR
TEMPLATES_ROOT = ROOT / site_config.TEMPLATES_DIR
DIST_ROOT = ROOT / site_config.DIST_DIR


@dataclass(frozen=True)
class Page:
    slug: str
    title: str
    description: str
    body_html: object
    sections: list
    index: int


def _static_page_url(slug: str) -> str:
    return "index.html" if slug == "home" else f"{slug}.html"


def _static_asset_url(name: str) -> str:
    return f"static/{name}"


def _load_pages() -> dict[str, Page]:
    converter = TinyMarkdown()
    pages: dict[str, Page] = {}
    for index, slug in enumerate(site_config.PAGE_ORDER, start=1):
        source = CONTENT_ROOT / f"{slug}.md"
        if not source.exists():
            raise SystemExit(f"ERROR: required content file is missing: {source}")
        rendered: RenderedMarkdown = converter.convert(source.read_text(encoding="utf-8"))
        pages[slug] = Page(
            slug=slug,
            title=rendered.title or site_config.NAV_LABELS.get(slug, slug),
            description=site_config.PAGE_DESCRIPTIONS.get(slug, ""),
            body_html=rendered.html,
            sections=list(rendered.sections),
            index=index,
        )
    return pages


def _reset_dist() -> None:
    if DIST_ROOT.exists():
        shutil.rmtree(DIST_ROOT)
    DIST_ROOT.mkdir(parents=True)


def _copy_static() -> None:
    dest = DIST_ROOT / site_config.STATIC_DIR
    if STATIC_ROOT.exists():
        shutil.copytree(STATIC_ROOT, dest)
    else:
        dest.mkdir(parents=True)


def build() -> list[str]:
    _reset_dist()
    _copy_static()

    pages = _load_pages()

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_ROOT)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template = env.get_template("base.html")

    written: list[str] = []
    for slug, page in pages.items():
        html = template.render(
            page=page,
            pages=pages,
            nav_order=site_config.PAGE_ORDER,
            nav_labels=site_config.NAV_LABELS,
            site_title=site_config.SITE_TITLE,
            site_description=site_config.SITE_DESCRIPTION,
            page_url=_static_page_url,
            asset_url=_static_asset_url,
        )
        out_name = _static_page_url(slug)
        (DIST_ROOT / out_name).write_text(html, encoding="utf-8")
        written.append(out_name)

    return written


def main() -> None:
    written = build()
    print(f"Built {len(written)} pages into {DIST_ROOT.relative_to(ROOT)}/")
    for name in written:
        print(f"- {name}")


if __name__ == "__main__":
    main()
