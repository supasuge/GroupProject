"""Local Flask preview server.

This is preview-only; the production artifact is the static site emitted
by ``build_static.py``. All Markdown is parsed once at startup and cached
in-process so that requests never re-read the content directory.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from flask import Flask, abort, render_template

import site_config
from tiny_markdown import RenderedMarkdown, TinyMarkdown


@dataclass(frozen=True)
class Page:
    slug: str
    title: str
    description: str
    body_html: object  # markupsafe.Markup
    sections: list
    index: int


def _load_pages(content_dir: Path) -> dict[str, Page]:
    converter = TinyMarkdown()
    pages: dict[str, Page] = {}
    for index, slug in enumerate(site_config.PAGE_ORDER, start=1):
        source = content_dir / f"{slug}.md"
        if not source.exists():
            raise FileNotFoundError(f"missing content file: {source}")
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


def create_app(content_dir: str | Path | None = None) -> Flask:
    root = Path(__file__).resolve().parent
    content_root = Path(content_dir) if content_dir else root / site_config.CONTENT_DIR

    app = Flask(
        __name__,
        static_folder=str(root / site_config.STATIC_DIR),
        template_folder=str(root / site_config.TEMPLATES_DIR),
        static_url_path="/static",
    )

    pages = _load_pages(content_root)

    def page_url(slug: str) -> str:
        if slug == "home":
            return "/"
        return f"/{slug}"

    def asset_url(name: str) -> str:
        return f"/static/{name}"

    @app.context_processor
    def _inject_globals() -> dict:
        return {
            "site_title": site_config.SITE_TITLE,
            "site_description": site_config.SITE_DESCRIPTION,
            "pages": pages,
            "nav_order": site_config.PAGE_ORDER,
            "nav_labels": site_config.NAV_LABELS,
            "page_url": page_url,
            "asset_url": asset_url,
        }

    def render_slug(slug: str):
        page = pages.get(slug)
        if page is None:
            abort(404)
        return render_template("base.html", page=page)

    @app.get("/")
    def home():
        return render_slug("home")

    @app.get("/<slug>")
    def show_page(slug: str):
        if slug not in pages or slug == "home":
            abort(404)
        return render_slug(slug)

    @app.errorhandler(404)
    def not_found(_error):
        # Use the home page chrome so 404s still feel like part of the site.
        home_page = pages["home"]
        return render_template("base.html", page=home_page), 404

    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)
