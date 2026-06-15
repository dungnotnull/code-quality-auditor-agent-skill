# test_knowledge_updater.py -- Unit tests for tools/knowledge_updater.py
# Tests deduplication, scoring, formatting, and brain-file appender logic.
#
# Run: python -m pytest tests/test_knowledge_updater.py -v
# Or:  python tests/test_knowledge_updater.py

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

# Import functions from knowledge_updater
from knowledge_updater import (
    KnowledgeEntry,
    _append_to_brain,
    _combined_score,
    _entry_hash,
    _format_entry,
    _load_seen_hashes,
    _relevance_score,
    _recency_score,
    _save_seen_hashes,
    BRAIN_FILE,
    STATE_FILE,
    MIN_RELEVANCE_SCORE,
    RECENCY_DAYS,
    RELEVANCE_KEYWORDS,
)


class TestEntryHash:
    """Test deduplication hash generation."""

    def test_deterministic(self):
        h1 = _entry_hash("https://arxiv.org/abs/2401.00001")
        h2 = _entry_hash("https://arxiv.org/abs/2401.00001")
        assert h1 == h2

    def test_unique_for_different_urls(self):
        h1 = _entry_hash("https://arxiv.org/abs/2401.00001")
        h2 = _entry_hash("https://arxiv.org/abs/2401.00002")
        assert h1 != h2

    def test_length_16(self):
        h = _entry_hash("https://example.com")
        assert len(h) == 16

    def test_empty_url(self):
        h = _entry_hash("")
        assert len(h) == 16

    def test_sha256_prefix(self):
        url = "https://arxiv.org/abs/2401.00001"
        expected = hashlib.sha256(url.encode()).hexdigest()[:16]
        assert _entry_hash(url) == expected


class TestRelevanceScore:
    """Test keyword-based relevance scoring."""

    def test_high_relevance(self):
        text = "Code quality and technical debt analysis using static analysis tools for maintainability"
        score = _relevance_score(text)
        assert score >= 2.0, f"Expected >= 2.0, got {score}"

    def test_low_relevance(self):
        text = "Quantum computing algorithms for optimization problems"
        score = _relevance_score(text)
        assert score <= 3.0

    def test_empty_text(self):
        score = _relevance_score("")
        assert score == 0.0

    def test_max_score_capped_at_10(self):
        text = " ".join(RELEVANCE_KEYWORDS)
        score = _relevance_score(text)
        assert score <= 10.0

    def test_security_keywords(self):
        text = "security vulnerability OWASP static analysis"
        score = _relevance_score(text)
        assert score >= 2.0

    def test_case_insensitive(self):
        text1 = "Code Quality Technical Debt"
        text2 = "code quality technical debt"
        assert _relevance_score(text1) == _relevance_score(text2)


class TestRecencyScore:
    """Test date-based recency scoring."""

    def test_today_is_10(self):
        today = datetime.now(tz=timezone.utc).isoformat()
        assert _recency_score(today) == 10.0

    def test_at_cutoff_is_0(self):
        old = (datetime.now(tz=timezone.utc) - timedelta(days=RECENCY_DAYS)).isoformat()
        assert _recency_score(old) == 0.0

    def test_midpoint_is_near_5(self):
        mid = (datetime.now(tz=timezone.utc) - timedelta(days=RECENCY_DAYS // 2)).isoformat()
        score = _recency_score(mid)
        assert 4.0 <= score <= 6.0, f"Expected 4.0-6.0, got {score}"

    def test_invalid_date(self):
        assert _recency_score("not-a-date") == 5.0

    def test_date_only_no_time(self):
        date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        score = _recency_score(date_str)
        assert score >= 9.0

    def test_future_date_capped_at_10(self):
        future = (datetime.now(tz=timezone.utc) + timedelta(days=30)).isoformat()
        score = _recency_score(future)
        assert score == 10.0


class TestCombinedScore:
    """Test combined relevance + recency scoring."""

    def test_high_relevance_recent(self):
        text = "code quality technical debt refactoring software metrics"
        date = datetime.now(tz=timezone.utc).isoformat()
        score = _combined_score(text, date)
        assert score >= 3.0

    def test_low_relevance_old(self):
        text = "quantum computing optimization"
        date = (datetime.now(tz=timezone.utc) - timedelta(days=int(RECENCY_DAYS * 0.9))).isoformat()
        score = _combined_score(text, date)
        assert score < 5.0

    def test_weight_distribution(self):
        text = "code quality"
        today = datetime.now(tz=timezone.utc).isoformat()
        score = _combined_score(text, today)
        rel = _relevance_score(text)
        rec = _recency_score(today)
        expected = round(rel * 0.6 + rec * 0.4, 1)
        assert abs(score - expected) < 0.2


class TestSeenHashes:
    """Test deduplication state persistence."""

    def test_load_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / ".crawl_state.json"
            with patch("knowledge_updater.STATE_FILE", state_file):
                hashes = _load_seen_hashes()
                assert hashes == set()

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / ".crawl_state.json"
            with patch("knowledge_updater.STATE_FILE", state_file):
                test_hashes = {"abc123", "def456"}
                _save_seen_hashes(test_hashes)
                loaded = _load_seen_hashes()
                assert loaded == test_hashes

    def test_overwrite(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / ".crawl_state.json"
            with patch("knowledge_updater.STATE_FILE", state_file):
                _save_seen_hashes({"abc123"})
                _save_seen_hashes({"xyz789"})
                loaded = _load_seen_hashes()
                assert loaded == {"xyz789"}


class TestFormatEntry:
    """Test markdown formatting of knowledge entries."""

    def test_basic_format(self):
        entry = KnowledgeEntry(
            title="Test Paper on Code Quality",
            authors="Smith, J.",
            date="2026-06-01",
            url="https://arxiv.org/abs/2401.00001",
            venue="ArXiv (cs.SE)",
            abstract="A study of code quality metrics and their impact on maintainability.",
            relevance_score=7.5,
            label="Code Quality & Technical Debt",
        )
        formatted = _format_entry(entry)
        assert "Test Paper on Code Quality" in formatted
        assert "Smith, J." in formatted
        assert "2026-06-01" in formatted
        assert "7.5/10" in formatted
        assert "https://arxiv.org/abs/2401.00001" in formatted

    def test_markdown_link(self):
        entry = KnowledgeEntry(
            title="My Paper",
            authors="Doe, J.",
            date="2026-01-01",
            url="https://example.com",
            venue="Web",
            abstract="Abstract text",
            relevance_score=6.0,
            label="Test",
        )
        formatted = _format_entry(entry)
        assert "[My Paper](https://example.com)" in formatted


class TestAppendToBrain:
    """Test SECOND-KNOWLEDGE-BRAIN.md file appender."""

    def _make_brain(self, tmpdir: Path) -> Path:
        brain = tmpdir / "SECOND-KNOWLEDGE-BRAIN.md"
        brain.write_text(
            "# SECOND-KNOWLEDGE-BRAIN.md\n\n"
            "## 2. Key Research Papers\n\n"
            "## 7. Knowledge Update Log\n\n"
            "| Date | Source | Entries Added | Notes |\n"
            "|---|---|---|---|\n"
            "| 2026-06-11 | Manual | 10 core | Initial |\n"
            "| _(pending)_ | knowledge_updater.py | TBD | First automated crawl run |\n",
            encoding="utf-8",
        )
        return brain

    def test_append_entries(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            brain_file = self._make_brain(Path(tmpdir))
            with patch("knowledge_updater.BRAIN_FILE", brain_file):
                entries = [
                    KnowledgeEntry(
                        title="Test Paper A",
                        authors="Author A",
                        date="2026-05-01",
                        url="https://arxiv.org/abs/2401.00001",
                        venue="ArXiv (cs.SE)",
                        abstract="Abstract A about code quality and technical debt.",
                        relevance_score=8.0,
                        label="Code Quality",
                    ),
                    KnowledgeEntry(
                        title="Test Paper B",
                        authors="Author B",
                        date="2026-04-15",
                        url="https://arxiv.org/abs/2401.00002",
                        venue="ArXiv (cs.SE)",
                        abstract="Abstract B about static analysis tools.",
                        relevance_score=6.5,
                        label="Static Analysis",
                    ),
                ]
                _append_to_brain(entries)
                content = brain_file.read_text(encoding="utf-8")
                assert "Test Paper A" in content
                assert "Test Paper B" in content
                assert "8.0/10" in content
                assert "6.5/10" in content
                assert "2 new entries" in content

    def test_append_empty_does_nothing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            brain_file = self._make_brain(Path(tmpdir))
            original = brain_file.read_text(encoding="utf-8")
            with patch("knowledge_updater.BRAIN_FILE", brain_file):
                _append_to_brain([])
                after = brain_file.read_text(encoding="utf-8")
                assert original == after

    def test_sorted_by_relevance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            brain_file = self._make_brain(Path(tmpdir))
            with patch("knowledge_updater.BRAIN_FILE", brain_file):
                entries = [
                    KnowledgeEntry(
                        title="Low Score",
                        authors="A",
                        date="2026-05-01",
                        url="https://example.com/low",
                        venue="Web",
                        abstract="Low",
                        relevance_score=4.0,
                        label="Test",
                    ),
                    KnowledgeEntry(
                        title="High Score",
                        authors="B",
                        date="2026-05-01",
                        url="https://example.com/high",
                        venue="Web",
                        abstract="High",
                        relevance_score=9.0,
                        label="Test",
                    ),
                ]
                _append_to_brain(entries)
                content = brain_file.read_text(encoding="utf-8")
                high_pos = content.find("High Score")
                low_pos = content.find("Low Score")
                assert high_pos < low_pos


class TestArxivFetcher:
    """Test ArXiv entry fetching (mocked)."""

    def test_fetch_with_mock(self):
        mock_result_1 = MagicMock()
        mock_result_1.entry_id = "https://arxiv.org/abs/2401.00001"
        mock_result_1.title = "Code Quality Analysis Using Static Analysis"
        mock_result_1.summary = "We present a novel approach to code quality assessment using static analysis and software metrics for maintainability."
        mock_result_1.published = datetime.now(tz=timezone.utc) - timedelta(days=5)
        mock_result_1.authors = [MagicMock(__str__=lambda self: "Author1"), MagicMock(__str__=lambda self: "Author2")]
        mock_result_1.categories = ["cs.SE", "cs.PL"]

        mock_result_2 = MagicMock()
        mock_result_2.entry_id = "https://arxiv.org/abs/2401.00002"
        mock_result_2.title = "Unrelated Paper on Quantum Computing"
        mock_result_2.summary = "Quantum algorithms for combinatorial optimization problems."
        mock_result_2.published = datetime.now(tz=timezone.utc) - timedelta(days=10)
        mock_result_2.authors = [MagicMock(__str__=lambda self: "Author3")]
        mock_result_2.categories = ["quant-ph"]

        mock_search = MagicMock()
        mock_search.__iter__ = lambda self: iter([mock_result_1, mock_result_2])

        mock_client = MagicMock()
        mock_client.results.return_value = [mock_result_1, mock_result_2]

        with patch("knowledge_updater.arxiv.Search", return_value=mock_search), \
             patch("knowledge_updater.arxiv.Client", return_value=mock_client):
            from knowledge_updater import _fetch_arxiv_entries
            seen = set()
            entries = _fetch_arxiv_entries(seen)
            for entry in entries:
                assert entry["relevance_score"] >= MIN_RELEVANCE_SCORE
                assert "code quality" in entry["abstract"].lower() or \
                       "static analysis" in entry["abstract"].lower() or \
                       "maintainability" in entry["abstract"].lower()


class TestWebCrawler:
    """Test web entry fetching (mocked)."""

    def test_crawl_with_mock(self):
        from unittest.mock import AsyncMock

        mock_crawl_result = MagicMock()
        mock_crawl_result.success = True
        mock_crawl_result.markdown = (
            "# Refactoring Guru Catalog\n\n"
            "A comprehensive catalog of code refactoring patterns and code smell detection techniques "
            "for improving software maintainability and code quality."
        )

        mock_crawler_instance = MagicMock()
        mock_crawler_instance.arun = AsyncMock(return_value=mock_crawl_result)
        mock_crawler_instance.__aenter__ = AsyncMock(return_value=mock_crawler_instance)
        mock_crawler_instance.__aexit__ = AsyncMock(return_value=None)

        with patch("knowledge_updater.AsyncWebCrawler", return_value=mock_crawler_instance):
            from knowledge_updater import _fetch_web_entries
            seen = set()
            entries = asyncio.run(_fetch_web_entries(seen))
            for entry in entries:
                assert entry["url"]
                assert entry["relevance_score"] >= MIN_RELEVANCE_SCORE
                assert entry["authors"] == "(Web resource)"


class TestMinRelevanceThreshold:
    """Ensure MIN_RELEVANCE_SCORE is reasonable."""

    def test_threshold_is_set(self):
        assert MIN_RELEVANCE_SCORE >= 3.0
        assert MIN_RELEVANCE_SCORE <= 8.0

    def test_recency_days_is_positive(self):
        assert RECENCY_DAYS > 0


class TestKnowledgeEntrySchema:
    """Test the KnowledgeEntry TypedDict has all required fields."""

    def test_create_entry(self):
        entry = KnowledgeEntry(
            title="Test",
            authors="Test Author",
            date="2026-01-01",
            url="https://example.com",
            venue="Test Venue",
            abstract="Test abstract",
            relevance_score=7.0,
            label="Test Label",
        )
        assert entry["title"] == "Test"
        assert entry["relevance_score"] == 7.0


class TestScheduleCron:
    """Test schedule_cron.py dry-run mode."""

    def test_dry_run_import(self):
        sys.path.insert(0, str(PROJECT_ROOT / "tools"))
        from schedule_cron import _setup, _uninstall
        assert callable(_setup)
        assert callable(_uninstall)


class TestContentCleaning:
    """Test web content cleaning functions."""

    def test_clean_ad_content(self):
        from knowledge_updater import _clean_web_content
        dirty = "Check out my new Git course! Hey! This is real content about code quality."
        cleaned = _clean_web_content(dirty)
        assert "Git course" not in cleaned
        assert "code quality" in cleaned

    def test_extract_meaningful_abstract(self):
        from knowledge_updater import _extract_meaningful_abstract
        content = "# Title\n\nShort line.\n\nThis is a meaningful paragraph about software quality and technical debt analysis that should be extracted as the abstract because it is long enough."
        abstract = _extract_meaningful_abstract(content)
        assert "software quality" in abstract
        assert "technical debt" in abstract


def run_tests():
    """Run all tests without pytest (fallback runner)."""
    test_classes = [
        TestEntryHash,
        TestRelevanceScore,
        TestRecencyScore,
        TestCombinedScore,
        TestSeenHashes,
        TestFormatEntry,
        TestAppendToBrain,
        TestArxivFetcher,
        TestWebCrawler,
        TestMinRelevanceThreshold,
        TestKnowledgeEntrySchema,
        TestScheduleCron,
        TestContentCleaning,
    ]

    passed = 0
    failed = 0
    errors = []

    for cls in test_classes:
        instance = cls()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    getattr(instance, method_name)()
                    passed += 1
                    print(f"  PASS: {cls.__name__}.{method_name}")
                except Exception as e:
                    failed += 1
                    errors.append((cls.__name__, method_name, str(e)))
                    print(f"  FAIL: {cls.__name__}.{method_name} -- {e}")

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    if errors:
        print("\nFailures:")
        for cls_name, method, err in errors:
            print(f"  {cls_name}.{method}: {err}")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
