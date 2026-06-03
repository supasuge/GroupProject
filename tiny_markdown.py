"""A small, defensive Markdown -> HTML converter.

Supports only the syntax the project needs:
  H1..H3, paragraphs, unordered lists, bold/italic, links, images, hr,
  blockquotes. Raw HTML inside Markdown is escaped to text rather than
  passed through.

Security posture:
  * All raw text is escaped through ``markupsafe.escape`` BEFORE any
    Markdown transforms run.
  * Only an allow-list of URL shapes is permitted for links and images
    (``http(s)://``, fragment ``#...``, or relative paths without a
    scheme). ``javascript:``, ``data:``, and parent-directory traversal
    are rejected.
  * Image sources must live under ``static/images/``.
  * External links automatically receive ``rel="noopener noreferrer"``
    and ``target="_blank"``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

from markupsafe import Markup, escape


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Section:
    id: str
    title: str
    level: int


@dataclass(frozen=True)
class RenderedMarkdown:
    html: Markup
    sections: list[Section] = field(default_factory=list)
    title: str = ""


# ---------------------------------------------------------------------------
# Inline element regexes (operate on already-escaped text)
# ---------------------------------------------------------------------------

# markupsafe.escape rewrites & < > " ' but leaves brackets, parens, asterisks,
# underscores, hashes, hyphens, and exclamation marks alone, so the markdown
# delimiters survive the escape pass.

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_IMAGE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$")
_BOLD_RE = re.compile(r"\*\*([^*\n]+)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")

_SAFE_RELATIVE_RE = re.compile(r"^[A-Za-z0-9_./#?=&%\-]+$")
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$")
_HR_RE = re.compile(r"^-{3,}\s*$")
_LIST_ITEM_RE = re.compile(r"^[-*]\s+(.+)$")
_BLOCKQUOTE_RE = re.compile(r"^>\s?(.*)$")


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def _is_safe_link_url(url: str) -> bool:
    lowered = url.strip().lower()
    if not lowered:
        return False
    if lowered.startswith("javascript:") or lowered.startswith("data:") or lowered.startswith("vbscript:"):
        return False
    if lowered.startswith(("http://", "https://", "mailto:")):
        return True
    if lowered.startswith("#"):
        return True
    if ".." in url:
        return False
    # Relative path: must not contain a scheme.
    if ":" in url.split("/", 1)[0]:
        return False
    return bool(_SAFE_RELATIVE_RE.match(url))


def _is_safe_image_url(url: str) -> bool:
    if ".." in url:
        return False
    if "://" in url or url.startswith(("javascript:", "data:")):
        return False
    return url.startswith("static/images/")


def _render_link(match: re.Match[str]) -> str:
    label = match.group(1)
    url = match.group(2)
    if not _is_safe_link_url(url):
        return f"[{label}]({escape(url)})"
    safe_url = escape(url)
    is_external = url.lower().startswith(("http://", "https://"))
    if is_external:
        return (
            f'<a href="{safe_url}" target="_blank" rel="noopener noreferrer">'
            f"{label}</a>"
        )
    return f'<a href="{safe_url}">{label}</a>'


def _apply_inline(text: str) -> str:
    # text is already escaped.
    text = _LINK_RE.sub(_render_link, text)
    text = _BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = _ITALIC_RE.sub(r"<em>\1</em>", text)
    return text


def _render_image_block(alt: str, src: str) -> str | None:
    if not _is_safe_image_url(src):
        return None
    safe_alt = escape(alt or "")
    safe_src = escape(src)
    alt_attr = f' alt="{safe_alt}"'
    return (
        '<figure class="content-figure">'
        f'<img src="{safe_src}"{alt_attr} loading="lazy" decoding="async">'
        + (f"<figcaption>{safe_alt}</figcaption>" if alt else "")
        + "</figure>"
    )


# ---------------------------------------------------------------------------
# Block-level parser
# ---------------------------------------------------------------------------


def _group_blocks(lines: Iterable[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for raw in lines:
        line = raw.rstrip("\n").rstrip("\r")
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


class TinyMarkdown:
    """Render a small, allow-listed Markdown dialect to HTML."""

    def convert(self, markdown: str) -> RenderedMarkdown:
        blocks = _group_blocks(markdown.splitlines())
        sections: list[Section] = []
        seen_ids: dict[str, int] = {}
        title = ""
        out: list[str] = []

        for block in blocks:
            first = block[0]
            heading_match = _HEADING_RE.match(first) if len(block) == 1 else None

            if heading_match:
                hashes, raw_title = heading_match.groups()
                level = len(hashes)
                clean_title = raw_title.strip()
                escaped_title_for_attr = _apply_inline(str(escape(clean_title)))
                base_slug = _slugify(clean_title)
                count = seen_ids.get(base_slug, 0) + 1
                seen_ids[base_slug] = count
                slug = base_slug if count == 1 else f"{base_slug}-{count}"
                if level == 1 and not title:
                    title = clean_title
                if level in (2, 3):
                    sections.append(Section(id=slug, title=clean_title, level=level))
                if level == 1:
                    # h1 still rendered but the template usually hides it in the card;
                    # we keep it for accessibility & semantic structure.
                    out.append(
                        f'<h1 id="{slug}" class="md-h1">{escaped_title_for_attr}</h1>'
                    )
                else:
                    out.append(
                        f'<h{level} id="{slug}" class="md-h{level}">'
                        f"<a class=\"heading-anchor\" href=\"#{slug}\" aria-hidden=\"true\" tabindex=\"-1\">#</a>"
                        f"{escaped_title_for_attr}</h{level}>"
                    )
                continue

            if len(block) == 1 and _HR_RE.match(first):
                out.append('<hr class="md-hr">')
                continue

            if len(block) == 1:
                image_match = _IMAGE_RE.match(first)
                if image_match:
                    alt, src = image_match.groups()
                    figure = _render_image_block(alt, src)
                    if figure is not None:
                        out.append(figure)
                        continue
                    # fall through to paragraph rendering if unsafe

            if all(_LIST_ITEM_RE.match(line) for line in block):
                items = []
                for line in block:
                    match = _LIST_ITEM_RE.match(line)
                    assert match is not None
                    item_text = _apply_inline(str(escape(match.group(1))))
                    items.append(f"<li>{item_text}</li>")
                out.append('<ul class="md-list">' + "".join(items) + "</ul>")
                continue

            if all(_BLOCKQUOTE_RE.match(line) for line in block):
                inner_lines = []
                for line in block:
                    match = _BLOCKQUOTE_RE.match(line)
                    assert match is not None
                    inner_lines.append(match.group(1))
                inner_text = " ".join(line.strip() for line in inner_lines if line.strip())
                inner_html = _apply_inline(str(escape(inner_text)))
                out.append(f'<blockquote class="md-quote"><p>{inner_html}</p></blockquote>')
                continue

            # Default: paragraph; join wrapped lines with a single space.
            paragraph_text = " ".join(line.strip() for line in block)
            paragraph_html = _apply_inline(str(escape(paragraph_text)))
            out.append(f"<p>{paragraph_html}</p>")

        html = Markup("\n".join(out))
        return RenderedMarkdown(html=html, sections=sections, title=title)


__all__ = ["TinyMarkdown", "RenderedMarkdown", "Section"]
