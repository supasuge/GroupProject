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
    author_text = ", ".join(authors)
    return author_text if author_text.endswith(".") else f"{author_text}."


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
    "manutd_homepage": AcademicSource(
        key="manutd_homepage",
        authors=("Manchester United",),
        year="n.d.",
        title="Official Manchester United website",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Manchester United Football Club",
        url="https://www.manutd.com/en",
        retrieval_date="June 17, 2026",
    ),
    # --- Sources cited in the group project document ---
    "bandura2023": AcademicSource(
        key="bandura2023",
        authors=("Bandura et al",),
        year="2023",
        title="Alcohol consumption among UK football supporters: Investigating the contested field of the football carnivalesque",
        source_type=SourceType.JOURNAL,
        site_or_journal="Drugs: Education, Prevention and Policy, 2024, v. 31",
        url="https://www.tandfonline.com/doi/full/10.1080/09687637.2023.2219370",
    ),
    "armstrong1998": AcademicSource(
        key="armstrong1998",
        authors=("Armstrong, G.",),
        year="1998",
        title="Football hooligans: Knowing the score",
        source_type=SourceType.BOOK,
        publisher="Berg",
    ),
    "wikipedia_football_england": AcademicSource(
        key="wikipedia_football_england",
        authors=("Wikipedia contributors",),
        year="n.d.",
        title="Football in England",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Wikipedia",
        url="https://en.wikipedia.org/wiki/Football_in_England",
    ),
    # --- Manchester United history ---
    "manutd_official_history": AcademicSource(
        key="manutd_official_history",
        authors=("Manchester United",),
        year="n.d.",
        title="Club history",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Manchester United Football Club",
        url="https://www.manutd.com/en/news/club-history",
    ),
    "britannica_manutd": AcademicSource(
        key="britannica_manutd",
        authors=("Gifford, C.",),
        year="2026",
        title="Manchester United",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Encyclopaedia Britannica",
        url="https://www.britannica.com/topic/Manchester-United",
    ),
    "men_iconic_manutd_photos": AcademicSource(
        key="men_iconic_manutd_photos",
        authors=("Manchester Evening News",),
        year="n.d.",
        title="100 iconic Manchester United pictures",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Manchester Evening News",
        url="https://www.manchestereveningnews.co.uk/sport/football/football-news/gallery/100-iconic-manchester-united-pictures-4869374",
    ),
    "premierleague_history": AcademicSource(
        key="premierleague_history",
        authors=("Premier League",),
        year="n.d.",
        title="History and statistics",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Premier League",
        url="https://www.premierleague.com/history",
    ),
    "uefa_history": AcademicSource(
        key="uefa_history",
        authors=("UEFA",),
        year="n.d.",
        title="UEFA Champions League history",
        source_type=SourceType.WEBPAGE,
        site_or_journal="UEFA",
        url="https://www.uefa.com/uefachampionsleague/history/",
    ),
    "bbc_charlton2023": AcademicSource(
        key="bbc_charlton2023",
        authors=("BBC News",),
        year="2023",
        title="Sir Bobby Charlton: Manchester United and England great dies aged 86",
        source_type=SourceType.WEBPAGE,
        site_or_journal="BBC News",
        url="https://www.bbc.com/news/uk-67166953",
    ),
    "guardian_manutd": AcademicSource(
        key="guardian_manutd",
        authors=("The Guardian",),
        year="n.d.",
        title="Manchester United: Archive coverage of the 2005 Glazer takeover and the 2021 European Super League proposals",
        source_type=SourceType.WEBPAGE,
        site_or_journal="The Guardian",
        url="https://www.theguardian.com/football/manchester-united",
    ),
    # --- English soccer and culture ---
    "fa_history": AcademicSource(
        key="fa_history",
        authors=("The Football Association",),
        year="n.d.",
        title="The history of The FA",
        source_type=SourceType.WEBPAGE,
        site_or_journal="The Football Association",
        url="https://www.thefa.com/about-football-association/what-we-do/history",
    ),
    "efl_history": AcademicSource(
        key="efl_history",
        authors=("English Football League",),
        year="n.d.",
        title="EFL history",
        source_type=SourceType.WEBPAGE,
        site_or_journal="English Football League",
        url="https://www.efl.com/about-the-efl/",
    ),
    "commonslibrary_regulator": AcademicSource(
        key="commonslibrary_regulator",
        authors=("House of Commons Library",),
        year="n.d.",
        title="Independent regulator for English football",
        source_type=SourceType.REPORT,
        publisher="UK Parliament",
        url="https://commonslibrary.parliament.uk/research-briefings/cbp-9686/",
    ),
    "kickitout": AcademicSource(
        key="kickitout",
        authors=("Kick It Out",),
        year="n.d.",
        title="About Kick It Out",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Kick It Out",
        url="https://www.kickitout.org/about",
    ),
    "hillsborough2012": AcademicSource(
        key="hillsborough2012",
        authors=("Hillsborough Independent Panel",),
        year="2012",
        title="The report of the Hillsborough Independent Panel",
        source_type=SourceType.REPORT,
        publisher="UK Government",
        url="https://www.gov.uk/government/publications/hillsborough-independent-panel-disclosed-material-and-report",
    ),
    # --- Stadium and supporter culture ---
    "inglis2005": AcademicSource(
        key="inglis2005",
        authors=("Inglis, S.",),
        year="2005",
        title="Engineering Archie: Archibald Leitch — football ground designer",
        source_type=SourceType.BOOK,
        publisher="English Heritage",
    ),
    "must_trust": AcademicSource(
        key="must_trust",
        authors=("Manchester United Supporters' Trust",),
        year="n.d.",
        title="About MUST",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Manchester United Supporters' Trust",
        url="https://joinmust.org/",
    ),
    "fcunited": AcademicSource(
        key="fcunited",
        authors=("FC United of Manchester",),
        year="n.d.",
        title="About: Club history",
        source_type=SourceType.WEBPAGE,
        site_or_journal="FC United of Manchester",
        url="https://www.fc-utd.co.uk/about",
    ),
    "bbc_rashford": AcademicSource(
        key="bbc_rashford",
        authors=("BBC Sport",),
        year="2020",
        title="Marcus Rashford: Free school meals campaign timeline",
        source_type=SourceType.WEBPAGE,
        site_or_journal="BBC Sport",
        url="https://www.bbc.com/sport/football/54693692",
    ),
    "sportscroll_protest": AcademicSource(
        key="sportscroll_protest",
        authors=("Mitchell, S.",),
        year="2026",
        title="Manchester United's History of Protest: Fans, Ownership, Identity",
        source_type=SourceType.WEBPAGE,
        site_or_journal="Sport Scroll",
        url="https://sportscroll.com/manchester-uniteds-long-legacy-of-protest-fans-ownership-and-the-fight-for-club-identity-ml3ak0ay",
    ),
    "sigodo2021": AcademicSource(
        key="sigodo2021",
        authors=("Sigodo, M.",),
        year="2021",
        title="Racism in Football: How Black coaches are tackling racism in the sport",
        source_type=SourceType.WEBPAGE,
        site_or_journal="MyLondon",
        url="https://www.mylondon.news/news/uk-world-news/diversity-british-football-still-lacking-21819248",
    ),
    "hamil2008": AcademicSource(
        key="hamil2008",
        authors=("Hamil, S.",),
        year="2008",
        title="Case 9 - Manchester United: the commercial development of a global football brand",
        source_type=SourceType.JOURNAL,
        site_or_journal="ScienceDirect",
        url="https://www.sciencedirect.com/science/chapter/edited-volume/abs/pii/B9780750685436500147?via%3Dihub",
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
