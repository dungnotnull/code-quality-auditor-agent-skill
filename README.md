# 🔍 Code Quality Auditor

> **A production-grade AI skill that transforms any source code repository into a structured, multi-dimensional professional audit report.**

[![Phase](https://img.shields.io/badge/Phase-Production%20Ready%20v1.0-green)]()
[![Tests](https://img.shields.io/badge/Tests-5%2F5%20Scenarios%20Passing-brightgreen)]()
[![Framework](https://img.shields.io/badge/Framework-ISO%2FIEC%2025010%3A2023-blue)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

---

## 🎯 What It Does

Give this skill any source code repository and it produces a **scored, professional audit report** covering:

| Dimension | What It Audits | Standard |
|---|---|---|
| **Maintainability** | SOLID violations, code duplication, naming, dead code | Clean Code / Martin |
| **Reliability** | Unhandled exceptions, null risks, race conditions | ISO 25010 |
| **Security** | OWASP Top 10, hardcoded secrets, injection risks, CSRF | OWASP 2021 |
| **Performance** | N+1 queries, O(n²) loops, blocking I/O, memory leaks | Empirical |
| **Testability** | Tight coupling, god objects, missing DI, static state | Martin / Feathers |
| **Complexity** | Cyclomatic complexity, cognitive complexity, LCOM, coupling | McCabe / SonarSource |

**But it doesn't stop at technical quality.** The skill also traces **business logic** — auditing whether the code correctly and completely implements the business rules — because a method with perfect cyclomatic complexity can still compute a refund incorrectly.

**The output is not a linting report.** It's a strategic assessment with:
- 📊 **Dimensional scores** (0–100) with calibration anchors
- 📋 **Evidence-grounded findings** with file:line references
- 🎯 **ROI-weighted improvement roadmap** (Quick Win → Strategic)
- ✅ **Devil's Advocate review** that challenges every finding before you see it

---

## 🏗️ Architecture

`
Source Code + Context
        │
        ▼
┌──────────────────────┐
│  Stage 0: Intake     │  Confirm scope, language, domain
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 1: Framework   │  ← sub-evaluation-framework-selector
│  Selection            │     ISO 25010 chars, tools, weights
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 2: Business    │  ← sub-business-logic-tracer
│  Logic Tracing        │     Flow map, [BL] findings
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 3: Technical   │  Direct analysis across 6 dimensions
│  Quality Analysis      │     [TQ] findings
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 4: Scoring     │  ← sub-scoring-engine
│                       │     Dimensional scores + composite
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 5: Devil's     │  Challenge findings, calibrate scores
│  Advocate Review      │     Quality gate — not skippable
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 6: Roadmap     │  ← sub-improvement-roadmap
│                       │     4-horizon plan with ROI narratives
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 7: Report      │  Professional markdown audit report
│  Assembly             │     Quality gates checklist
└──────────────────────┘
`

---

## 📂 Project Structure

`
code-quality-auditor/
├── CLAUDE.md                              # Skill-level memory & overview
├── PROJECT-detail.md                      # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Phase-by-phase build tracker
├── SECOND-KNOWLEDGE-BRAIN.md             # Self-improving domain knowledge base
├── README.md                              # This file
│
├── skills/
│   ├── main.md                            # 🎯 Main harness — 7-stage audit workflow
│   ├── sub-evaluation-framework-selector.md  # Framework & tool selection
│   ├── sub-business-logic-tracer.md       # Business flow tracing & BL findings
│   ├── sub-scoring-engine.md              # Finding-to-score deduction engine
│   └── sub-improvement-roadmap.md         # ROI-weighted prioritized roadmap
│
├── tools/
│   ├── knowledge_updater.py               # ArXiv + web crawler for KB updates
│   └── schedule_cron.py                   # Cross-platform cron scheduler
│
└── tests/
    ├── test-scenarios.md                  # 5 scenario-based test cases
    ├── test_knowledge_updater.py          # 36 unit tests for knowledge pipeline
    ├── run_audit_tests.py                 # Automated test harness
    ├── cross-skill-compatibility-report.md  # Cluster B validation
    ├── execution_logs/                    # Scenario execution results
    │   ├── scenario-1-execution-log.md
    │   ├── scenario-2-execution-log.md
    │   ├── scenario-3-execution-log.md
    │   ├── scenario-4-execution-log.md
    │   ├── scenario-5-execution-log.md
    │   └── gaps-and-fixes.md
    │
    └── mock_repos/                        # Intentionally flawed test codebases
        ├── django-ecommerce/              # Python Django (17 findings, 71/100)
        ├── react-admin-dashboard/         # React+TS (4 findings, 70/100)
        ├── spring-fintech-payment/        # Java Spring Boot (5 findings, 78/100)
        ├── node-hr-api/                   # Node.js Express (7 findings, 70/100)
        └── legacy-php-ecommerce/          # PHP 5.6 procedural (17 findings, 37/100)
`

---

## 🚀 Quick Start

### As an AI Skill (Claude / Codex)

The skill is invoked through the main harness file:

`
→ Invoke /code-quality-auditor with source code
`

Claude will follow the 7-stage workflow in skills/main.md, invoking each sub-skill in sequence and producing a professional audit report.

### Knowledge Pipeline

`ash
# Install dependencies
pip install crawl4ai httpx arxiv python-dotenv

# Run the knowledge updater (crawls ArXiv + web sources)
python tools/knowledge_updater.py

# Set up weekly cron (dry-run first)
python tools/schedule_cron.py --dry-run

# Set up for real
python tools/schedule_cron.py
`

### Running Tests

`ash
# Unit tests for knowledge_updater.py
python tests/test_knowledge_updater.py

# Automated audit test harness (all 5 scenarios)
python tests/run_audit_tests.py

# Single scenario
python tests/run_audit_tests.py --scenario 1
`

---

## 📊 Test Results

All 5 test scenarios produce valid reports that pass the 8 quality gates:

| Scenario | Language | Findings | Critical | Composite Score | Status |
|---|---|---|---|---|---|
| 1 — Django E-Commerce | Python | 17 | 4 | **71/100** (Fair) | ✅ Pass |
| 2 — React+TS Dashboard | TypeScript | 4 | 4 | **70/100** (Fair) | ✅ Pass |
| 3 — Spring Boot Fintech | Java | 5 | 4 | **78/100** (Good) | ✅ Pass |
| 4 — Node.js HR API | JavaScript | 7 | 1 | **70/100** (Fair) | ✅ Pass |
| 5 — Legacy PHP E-Commerce | PHP | 17 | 16 | **37/100** (Critical) | ✅ Pass |

### Quality Gates Checklist

| Gate | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| Evidence-grounded findings | ✅ | ✅ | ✅ | ✅ | ✅ |
| Named principle violations | ✅ | ✅ | ✅ | ✅ | ✅ |
| Score consistency | ✅ | ✅ | ✅ | ✅ | ✅ |
| Business logic coverage | ✅ | ✅ | ✅ | ✅ | ✅ |
| Devil's advocate review | ✅ | ✅ | ✅ | ✅ | ✅ |
| Quick win present | ✅ | ✅ | ✅ | ✅ | ✅ |
| Security OWASP refs | ✅ | ✅ | ✅ | ✅ | ✅ |
| Professional output | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🔬 Scoring Methodology

The scoring engine uses a **finding-based deduction system** grounded in ISO/IEC 25010:2023:

| Finding Severity | Points Deducted |
|---|---|
| Critical | −15 to −25 |
| Major | −5 to −10 |
| Minor | −1 to −3 |

**Calibration anchors** prevent score inflation/deflation:

| Score Range | Assessment |
|---|---|
| 90–100 | Excellent — follows best practices consistently |
| 75–89 | Good — well-structured with moderate issues |
| 60–74 | Fair — noticeable quality gaps, tech debt accumulating |
| 40–59 | Poor — multiple significant issues |
| 20–39 | Critical — pervasive quality problems |
| 0–19 | Failing — fundamental quality failures |

**Domain-specific weight adjustments** ensure relevance:

| Domain | Security Weight | Performance Weight | Maintainability Weight |
|---|---|---|---|
| General | 20% | 15% | 20% |
| Fintech/Healthcare | **30%** | 20% | 15% |
| Internal Tooling | 10% | **25%** | 25% |
| Public API | **25%** | 20% | 15% |

---

## 🧠 Self-Improving Knowledge Base

The SECOND-KNOWLEDGE-BRAIN.md is automatically updated weekly by knowledge_updater.py, which crawls:

- **ArXiv cs.SE** — Latest software engineering research papers
- **Refactoring.guru** — Code smell catalogs and refactoring patterns
- **Martin Fowler's Blog** — Architecture and technical debt insights
- **OWASP Top 10** — Security vulnerability references

Each entry is scored for **relevance** (keyword density against 18 quality terms) and **recency** (freshness decay over 90 days). Deduplication prevents re-crawling via URL hash checks.

---

## 🔗 Cluster B Integration

This skill is part of **Cluster B — Technical Evaluation Harnesses**, sharing three sub-skills with:

| Sub-Skill | Shared With | Compatibility |
|---|---|---|
| sub-evaluation-framework-selector | Skill 4 (uiux-code-auditor), Skill 8 (website-auditor) | ✅ — Added uiux & website domain profiles |
| sub-scoring-engine | Skill 4, Skill 8 | ✅ — Identical rubric across all 3 skills |
| sub-improvement-roadmap | Skill 4, Skill 8 | ✅ — Same priority formula & horizons |

Domain profiles for UI/UX and Website audits are already included in the framework selector, ensuring seamless cross-skill invocation.

---

## 🛡️ Quality Gates

Before any audit report is delivered, **8 quality gates must pass**:

1. ✅ Every finding references a **specific file:line** (no generic advice)
2. ✅ Every finding cites a **named standard** (ISO 25010, SOLID, OWASP, etc.)
3. ✅ Composite score is **mathematically consistent** with dimensional scores
4. ✅ Business logic trace covers **≥ 3 distinct user-facing flows**
5. ✅ Devil's advocate review was **completed and documented**
6. ✅ Improvement roadmap contains **≥ 1 Quick Win item**
7. ✅ Security findings reference **OWASP category or CVE**
8. ✅ Report reads as a **professional document**, not a chat transcript

---

## 📋 Improvement Roadmap Example

The roadmap uses a **priority formula** that any engineering manager can act on:

`
Priority = (Impact × 3) + (Urgency × 2) + (Ease × 1)
`

| Horizon | Priority Score | Timeline | Example |
|---|---|---|---|
| Quick Win | 18–30 | < 1 day | Remove hardcoded API key, fix bare excepts |
| Short-Term | 12–17 | 1–2 weeks | Fix N+1 queries, add idempotency keys |
| Medium-Term | 7–11 | 1–3 months | Decompose god classes, add test suites |
| Strategic | 1–6 | 3+ months | Architectural migration, full rewrite evaluation |

---

## 📦 Dependencies

### Knowledge Pipeline
`ash
pip install crawl4ai httpx arxiv python-dotenv
`

### Test Harness
`ash
python tests/run_audit_tests.py              # All scenarios
python tests/run_audit_tests.py --scenario 3  # Single scenario
python tests/test_knowledge_updater.py        # Unit tests
`

### Cron Scheduler
`ash
python tools/schedule_cron.py --dry-run   # Preview
python tools/schedule_cron.py            # Set up
python tools/schedule_cron.py --uninstall # Remove
`

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **ISO/IEC 25010:2023** — Software quality model framework
- **OWASP Top 10 (2021)** — Web application security risk framework
- **Robert C. Martin** — Clean Code principles and SOLID design
- **McCabe (1976)** — Cyclomatic complexity foundation
- **SonarSource** — Cognitive complexity methodology

---

*Built with production-grade standards. Ready for open-source.*
