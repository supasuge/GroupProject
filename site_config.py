"""Centralized site metadata and page ordering."""

from __future__ import annotations

SITE_TITLE = "Manchester United Project"
SITE_DESCRIPTION = (
    "A class project exploring soccer culture in England and the history of "
    "Manchester United."
)

CONTENT_DIR = "content"
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
DIST_DIR = "dist"

PAGE_ORDER: list[str] = [
    "home",
    "country-england",
    "team-manchester-united",
    "sources",
]

NAV_LABELS: dict[str, str] = {
    "home": "Home",
    "country-england": "England",
    "team-manchester-united": "Manchester United",
    "sources": "Sources",
}

PAGE_DESCRIPTIONS: dict[str, str] = {
    "home": "Project overview and reading guide for a class exhibit on Manchester United and English soccer culture.",
    "country-england": "How English soccer became woven into the country's social, political, and economic life.",
    "team-manchester-united": "The history, identity, and global reach of Manchester United Football Club.",
    "sources": "Citations, references, and image credits used throughout the project.",
}
