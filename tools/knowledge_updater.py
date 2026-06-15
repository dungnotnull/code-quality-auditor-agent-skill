"""
knowledge_updater.py -- code-quality-auditor skill
Self-improving knowledge pipeline: crawls authoritative software engineering
sources and appends scored entries to SECOND-KNOWLEDGE-BRAIN.md.

Dependencies: crawl4ai, httpx, arxiv, python-dotenv
Schedule: Weekly cron (see schedule_cron.py for setup)
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TypedDict

# -- Third-party (install via: pip install crawl4ai httpx arxiv python-dotenv)
try:
    import arxiv
    import httpx
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing dependency: {e}\nRun: pip install crawl4ai httpx arxiv python-dotenv")
    sys.exit(1)

load_dotenv()

# -- Paths
SKILL_DIR = Path(__file__).parent.parent
BRAIN_FILE = SKILL_DIR / "SECOND-KNOWLEDGE-BRAIN.md"
STATE_FILE = SKILL_DIR / "tools" / ".crawl_state.json"

# -- Config
ARXIV_QUERIES = [
    {
        "query": "software quality analysis code smell technical debt refactoring",
        "categories": ["cs.SE"],
        "max_results": 30,
        "label": "Code Quality & Technical Debt",
    },
    {
        "query": "static analysis defect prediction program analysis machine learning",
        "categories": ["cs.SE"],
        "max_results": 20,
        "label": "Static Analysis & Defect Prediction",
    },
    {
        "query": "software metrics maintainability cyclomatic complexity ISO 25010",
        "categories": ["cs.SE"],
        "max_results": 15,
        "label": "Software Metrics",
    },
    {
        "query": "software security vulnerability OWASP code review testing",
        "categories": ["cs.SE", "cs.CR"],
        "max_results": 15,
        "label": "Software Security",
    },
    {
        "query": "code refactoring design patterns clean architecture SOLID",
        "categories": ["cs.SE"],
        "max_results": 15,
        "label": "Design Patterns & Architecture",
    },
]

WEB_SOURCES = [
    {
        'url': 'https://refactoring.guru/refactoring/catalog',
        'label': 'Refactoring Guru - Catalog',
        'keywords': ['refactoring', 'code smell', 'pattern'],
    },
    {
        'url': 'https://martinfowler.com/bliki/TechnicalDebt.html',
        'label': 'Martin Fowler - Technical Debt',
        'keywords': ['technical debt', 'code quality'],
    },
    {
        'url': 'https://owasp.org/www-project-top-ten/',
        'label': 'OWASP Top 10',
        'keywords': ['security', 'vulnerability', 'OWASP'],
    },
    {
        'url': 'https://owasp.org/www-project-application-security-verification-standard/',
        'label': 'OWASP ASVS',
        'keywords': ['security', 'verification', 'standard'],
    },
    {
        'url': 'https://en.wikipedia.org/wiki/Software_quality',
        'label': 'Wikipedia - Software Quality',
        'keywords': ['software quality', 'ISO 25010', 'metric'],
    },
    {
        'url': 'https://en.wikipedia.org/wiki/Technical_debt',
        'label': 'Wikipedia - Technical Debt',
        'keywords': ['technical debt', 'refactoring', 'software quality'],
    },
    {
        'url': 'https://martinfowler.com/bliki/CodeSmell.html',
        'label': 'Martin Fowler - Code Smell',
        'keywords': ['code smell', 'refactoring', 'clean code'],
    },
    {
        'url': 'https://www.redhat.com/en/topics/devops/what-is-technical-debt',
        'label': 'Red Hat - Technical Debt',
        'keywords': ['technical debt', 'refactoring', 'software quality'],
    },
    {
        'url': 'https://docs.sonarsource.com/sonarqube/latest/user-guide/rules/',
        'label': 'SonarQube Rules Guide',
        'keywords': ['code quality', 'static analysis', 'rule'],
    },
    {
        'url': 'https://www.jetbrains.com/help/pycharm/code-quality-analysis.html',
        'label': 'JetBrains - Code Quality Analysis',
        'keywords': ['code quality', 'static analysis', 'inspection'],
    },
]

# Valid ArXiv CS categories for filtering
VALID_ARXIV_CATEGORIES = {
    "cs.SE", "cs.PL", "cs.CR", "cs.AI", "cs.LG",
    "cs.DC", "cs.NI", "cs.SY",
}

RELEVANCE_KEYWORDS = [
    "code quality", "technical debt", "code smell", "refactoring",
    "cyclomatic complexity", "software metrics", "static analysis",
    "clean code", "SOLID", "ISO 25010", "maintainability", "testability",
    "security vulnerability", "OWASP", "defect prediction", "coupling",
    "cohesion", "cognitive complexity", "software reliability",
    "code review", "software testing", "design pattern",
    "software architecture", "code duplication", "dependency injection",
    "test coverage", "continuous integration", "code review",
]

RECENCY_DAYS = 180  # Extended to 180 days for broader coverage
MIN_RELEVANCE_SCORE = 4.0  # Out of 10; skip entries below this threshold


# -- Type definitions


class KnowledgeEntry(TypedDict):
    title: str
    authors: str
    date: str
    url: str
    venue: str
    abstract: str
    relevance_score: float
    label: str


# -- Deduplication helpers


def _load_seen_hashes() -> set[str]:
    if STATE_FILE.exists():
        return set(json.loads(STATE_FILE.read_text())["seen"])
    return set()


def _save_seen_hashes(seen: set[str]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"seen": list(seen)}, indent=2))


def _entry_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


# -- Relevance scoring


def _relevance_score(text: str) -> float:
    """Score 0-10 based on keyword density."""
    text_lower = text.lower()
    matches = sum(1 for kw in RELEVANCE_KEYWORDS if kw.lower() in text_lower)
    return min(10.0, round((matches / len(RELEVANCE_KEYWORDS)) * 20, 1))


def _recency_score(date_str: str) -> float:
    """Score 0-10 based on how recent the entry is."""
    try:
        pub_date = datetime.fromisoformat(date_str.split("T")[0])
        pub_date = pub_date.replace(tzinfo=timezone.utc)
        age_days = (datetime.now(tz=timezone.utc) - pub_date).days
        score = 10.0 - (age_days / RECENCY_DAYS) * 10
        return max(0.0, min(10.0, round(score, 1)))
    except (ValueError, AttributeError):
        return 5.0


def _combined_score(text: str, date_str: str) -> float:
    rel = _relevance_score(text)
    rec = _recency_score(date_str)
    return round(rel * 0.6 + rec * 0.4, 1)


# -- Content cleaning for web entries


def _clean_web_content(content: str) -> str:
    """Remove ad content, navigation, and noise from web-scraped content."""
    # Remove common ad/noise patterns
    noise_patterns = [
        r'!?\[.*?\]\(https://[^)]*\.(svg|webp|png|jpg|gif)\)',
        r'Check out my.*?!',
        r'Hey!.*?Check out.*?$',
        r'Cookie.*?policy',
        r'Subscribe.*?newsletter',
        r'Sign up.*?free',
    ]
    cleaned = content
    for pattern in noise_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
    # Remove excessive whitespace
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()


def _extract_meaningful_abstract(content: str, min_chars: int = 80) -> str:
    """Extract the first meaningful paragraph from cleaned web content."""
    cleaned = _clean_web_content(content)
    paragraphs = [
        p.strip()
        for p in cleaned.split("\n")
        if len(p.strip()) > min_chars and not p.strip().startswith('#')
           and not p.strip().startswith('![')
    ]
    if paragraphs:
        return paragraphs[0][:400] + "..."
    # Fallback: use any paragraph
    paragraphs = [p.strip() for p in cleaned.split("\n") if len(p.strip()) > 40]
    if paragraphs:
        return paragraphs[0][:400] + "..."
    return cleaned[:400] + "..."


# -- ArXiv crawler


def _fetch_arxiv_entries(seen: set[str]) -> list[KnowledgeEntry]:
    entries: list[KnowledgeEntry] = []
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=RECENCY_DAYS)

    for config in ARXIV_QUERIES:
        search = arxiv.Search(
            query=config["query"],
            max_results=config["max_results"],
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        for result in arxiv.Client().results(search):
            # Filter: only accept papers in valid CS categories
            result_categories = set(result.categories)
            if not result_categories.intersection(VALID_ARXIV_CATEGORIES):
                continue

            pub_date = result.published.replace(tzinfo=timezone.utc)
            if pub_date < cutoff:
                continue

            url = result.entry_id
            h = _entry_hash(url)
            if h in seen:
                continue

            text = f"{result.title} {result.summary}"
            score = _combined_score(text, result.published.isoformat())
            if score < MIN_RELEVANCE_SCORE:
                continue

            entries.append(
                KnowledgeEntry(
                    title=result.title,
                    authors=", ".join(str(a) for a in result.authors[:3])
                    + (" et al." if len(result.authors) > 3 else ""),
                    date=result.published.strftime("%Y-%m-%d"),
                    url=url,
                    venue=f"ArXiv ({', '.join(c for c in result.categories[:2] if c in VALID_ARXIV_CATEGORIES)})",
                    abstract=result.summary[:400].replace("\n", " ") + "...",
                    relevance_score=score,
                    label=config["label"],
                )
            )
            seen.add(h)

    return entries


# -- Web crawler (crawl4ai)


async def _fetch_web_entries(seen: set[str]) -> list[KnowledgeEntry]:
    entries: list[KnowledgeEntry] = []
    config = CrawlerRunConfig(
        word_count_threshold=50,
        excluded_tags=["nav", "footer", "header", "aside", "script", "style", "noscript"],
        only_text=True,
    )

    async with AsyncWebCrawler(verbose=False) as crawler:
        for source in WEB_SOURCES:
            url = source["url"]
            h = _entry_hash(url)
            if h in seen:
                continue

            try:
                result = await crawler.arun(url=url, config=config)
                if not result.success or not result.markdown:
                    continue

                content = result.markdown[:3000]
                score = _combined_score(
                    content + " ".join(source["keywords"]),
                    datetime.now(tz=timezone.utc).isoformat(),
                )
                if score < MIN_RELEVANCE_SCORE:
                    continue

                # Extract meaningful abstract (cleaned of ads)
                abstract = _extract_meaningful_abstract(content)

                # Attempt to extract page title from markdown
                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1) if title_match else source["label"]

                entries.append(
                    KnowledgeEntry(
                        title=title[:120],
                        authors="(Web resource)",
                        date=datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
                        url=url,
                        venue="Web",
                        abstract=abstract,
                        relevance_score=score,
                        label=source["label"],
                    )
                )
                seen.add(h)

            except Exception as exc:  # noqa: BLE001
                print(f"  [WARN] Failed to crawl {url}: {exc}")

    return entries


# -- Markdown formatter


def _format_entry(entry: KnowledgeEntry) -> str:
    return (
        f"\n### [{entry['title']}]({entry['url']})\n"
        f"**Authors:** {entry['authors']}  \n"
        f"**Date:** {entry['date']}  \n"
        f"**Source:** {entry['venue']}  \n"
        f"**Category:** {entry['label']}  \n"
        f"**Relevance Score:** {entry['relevance_score']}/10  \n"
        f"**Summary:** {entry['abstract']}\n"
        f"**Added:** {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')}\n"
    )


# -- SECOND-KNOWLEDGE-BRAIN.md appender


def _append_to_brain(entries: list[KnowledgeEntry]) -> None:
    if not entries:
        return

    brain_text = BRAIN_FILE.read_text(encoding="utf-8")

    # Find or create the "Key Research Papers" section
    section_header = "## 2. Key Research Papers"
    if section_header not in brain_text:
        brain_text += f"\n\n{section_header}\n"

    # Build new content block
    crawl_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    new_block = f"\n#### Auto-crawled entries -- {crawl_date}\n"
    for entry in sorted(entries, key=lambda e: e["relevance_score"], reverse=True):
        new_block += _format_entry(entry)

    # Append before the Knowledge Update Log
    log_header = "## 7. Knowledge Update Log"
    if log_header in brain_text:
        brain_text = brain_text.replace(
            log_header, new_block + "\n" + log_header
        )
    else:
        brain_text += new_block

    # Update the Knowledge Update Log table
    log_row = (
        f"| {crawl_date} | knowledge_updater.py | {len(entries)} new entries | "
        f"Automated weekly crawl |\n"
    )
    brain_text = re.sub(
        r"(\| _\(pending\)_.*\n)",
        log_row + r"\1",
        brain_text,
        count=1,
    )

    BRAIN_FILE.write_text(brain_text, encoding="utf-8")


# -- Main


async def _main() -> None:
    print("=== code-quality-auditor knowledge_updater.py ===")
    print(f"Brain file: {BRAIN_FILE}")
    print(f"Cutoff: last {RECENCY_DAYS} days")

    if not BRAIN_FILE.exists():
        print(f"ERROR: {BRAIN_FILE} not found. Run from the skill root directory.")
        sys.exit(1)

    seen = _load_seen_hashes()
    print(f"Loaded {len(seen)} previously seen entry hashes.")

    # Fetch ArXiv entries (synchronous)
    print("\n[1/2] Fetching ArXiv papers...")
    arxiv_entries = _fetch_arxiv_entries(seen)
    print(f"  > {len(arxiv_entries)} new qualifying ArXiv entries")

    # Fetch web entries (async)
    print("[2/2] Crawling web sources...")
    web_entries = await _fetch_web_entries(seen)
    print(f"  > {len(web_entries)} new qualifying web entries")

    all_entries = arxiv_entries + web_entries
    print(f"\nTotal new entries: {len(all_entries)}")

    if all_entries:
        _append_to_brain(all_entries)
        _save_seen_hashes(seen)
        print(f"v Appended {len(all_entries)} entries to {BRAIN_FILE.name}")
    else:
        print("No new entries to add. SECOND-KNOWLEDGE-BRAIN.md unchanged.")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(_main())


