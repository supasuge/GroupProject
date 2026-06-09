"""Small APA-style citation helpers for the class website.

This module intentionally avoids external dependencies. It supports the
limited source types used by the project and produces APA 7-like references
plus parenthetical/narrative in-text citations.

The rendered references should still be reviewed by a human before final
submission, especially for journal volume/issue/page data.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SourceType(StrEnum):
    JOURNAL = "journal"
    REPORT = "report"
    WEBPAGE = "webpage"
    BOOK = "book"


@dataclass(frozen=True)
class AcademicSource:
    key: str
    authors: tuple[str, ...]
    year: str
    title: str
    source_type: SourceType
    site_or_journal: str = ""
    publisher: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    url: str = ""
    retrieval_date: str = ""

    @property
    def citation_author(self) -> str:
        if not self.authors:
            return self.title
        if len(self.authors) == 1:
            return self.authors[0]
        if len(self.authors) == 2:
            return f"{self.authors[0]} & {self.authors[1]}"
        return f"{self.authors[0]} et al."

    def parenthetical(self) -> str:
        return f"({self.citation_author}, {self.year})"

    def narrative(self) -> str:
        return f"{self.citation_author} ({self.year})"

    def reference(self) -> str:
        authors = _format_authors(self.authors)
        date = f"({self.year})."
        title = _sentence_case_title(self.title)

        if self.source_type == SourceType.JOURNAL:
            journal = self.site_or_journal
            vol_issue = ""
            if self.volume and self.issue:
                vol_issue = f", {self.volume}({self.issue})"
            elif self.volume:
                vol_issue = f", {self.volume}"
            pages = f", {self.pages}" if self.pages else ""
            url = f" {self.url}" if self.url else ""
            return f"{authors} {date} {title}. {journal}{vol_issue}{pages}.{url}".strip()

        if self.source_type == SourceType.REPORT:
            publisher = self.publisher or self.site_or_journal
            url = f" {self.url}" if self.url else ""
            return f"{authors} {date} {title}. {publisher}.{url}".strip()

        if self.source_type == SourceType.BOOK:
            publisher = self.publisher or self.site_or_journal
            return f"{authors} {date} {title}. {publisher}.".strip()

        # Webpage
        site = f" {self.site_or_journal}." if self.site_or_journal else ""
        retrieval = f" Retrieved {self.retrieval_date}, from" if self.retrieval_date else ""
        url = f" {self.url}" if self.url else ""
        return f"{authors} {date} {title}.{site}{retrieval}{url}".strip()


def _format_authors(authors: tuple[str, ...]) -> str:
    if not authors:
        return "Unknown author."
    return ", ".join(authors) + "."


def _sentence_case_title(title: str) -> str:
    # Keep project-readable titles stable rather than aggressively lowercasing
    # proper nouns such as Manchester United, Premier League, or England.
    return title.rstrip(".")


SOURCES: dict[str, AcademicSource] = {
    "flanagan2025": AcademicSource(
        key="flanagan2025",
        authors=("Flanagan, C. A.",),
        year="2025",
        title="The Football Governance Act, the Independent Football Regulator, and the regulation of football finance in England",
        source_type=SourceType.JOURNAL,
        site_or_journal="The International Sports Law Journal",
        url="https://link.springer.com/article/10.1007/s40318-025-00326-8",
    ),
    "dcms2023": AcademicSource(
        key="dcms2023",
        authors=("Department for Culture, Media and Sport",),
        year="2023",
        title="A sustainable future: Reforming club football governance",
        source_type=SourceType.REPORT,
        publisher="UK Government",
        url="https://www.gov.uk/government/publications/a-sustainable-future-reforming-club-football-governance",
    ),
    "ukparliament2025": AcademicSource(
        key="ukparliament2025",
        authors=("United Kingdom Parliament",),
        year="2025",
        title="Football Governance Act 2025",
        source_type=SourceType.WEBPAGE,
        site_or_journal="UK Parliament",
        url="https://bills.parliament.uk/bills/3832",
    ),
    "premierleague2025": AcademicSource(
        key="premierleague2025",
        authors=("Premier League",),
        year="2025",
        title="Research shows Premier League's growing contribution to UK economy",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Premier League",
        url="https://www.premierleague.com/en/news/4461419/research-shows-premier-leagues-growing-contribution-to-uk-economy",
    ),
    "chattopadhyay2024": AcademicSource(
        key="chattopadhyay2024",
        authors=("Chattopadhyay, A.", "Abdul, A.", "Jain, S."),
        year="2024",
        title="The impact of foreign players in the English Premier League: A mathematical analysis",
        source_type=SourceType.REPORT,
        publisher="arXiv",
        url="https://arxiv.org/abs/2407.19285",
    ),
    "porter2008": AcademicSource(
        key="porter2008",
        authors=("Porter, C.",),
        year="2008",
        title="Manchester United, global capitalism and local resistance",
        source_type=SourceType.JOURNAL,
        site_or_journal="Belgeo",
        url="https://journals.openedition.org/belgeo/10271",
    ),
    "parliament2025softpower": AcademicSource(
        key="parliament2025softpower",
        authors=("Premier League",),
        year="2025",
        title="Written evidence: Pro-growth reforms and investment",
        source_type=SourceType.REPORT,
        publisher="UK Parliament Committees",
        url="https://committees.parliament.uk/writtenevidence/153524/html/",
    ),
    "manutd_history": AcademicSource(
        key="manutd_history",
        authors=("Manchester United",),
        year="n.d.",
        title="History",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Manchester United Investor Relations",
        url="https://ir.manutd.com/company-information/history.aspx",
    ),
}


def cite(key: str) -> str:
    """Return an APA-style parenthetical citation for a source key."""
    return SOURCES[key].parenthetical()


def cite_narrative(key: str) -> str:
    """Return an APA-style narrative citation for a source key."""
    return SOURCES[key].narrative()


def reference_list(keys: list[str] | None = None) -> list[str]:
    """Return formatted references sorted alphabetically by citation author."""
    selected = [SOURCES[k] for k in (keys or list(SOURCES))]
    selected.sort(key=lambda src: src.citation_author.lower())
    return [src.reference() for src in selected]


if __name__ == "__main__":
    for ref in reference_list():
        print(ref)
