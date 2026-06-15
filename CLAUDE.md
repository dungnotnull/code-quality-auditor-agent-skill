---
name: code-quality-auditor
tagline: Comprehensive multi-dimensional source code quality and business logic audit
phase: Production Ready (v1.0)
cluster: B — Technical Evaluation Harnesses
---

## Problem This Skill Solves

Development teams accumulate technical debt without a systematic way to measure, prioritize, or communicate code quality issues to stakeholders. This skill gives any developer, tech lead, or CTO a structured, evidence-based audit of their codebase across both technical dimensions (architecture, maintainability, security, performance) and business logic dimensions (correctness, completeness, traceability to requirements).

The output is a scored professional report with a prioritized improvement roadmap — not a list of linting warnings, but a strategic assessment grounded in world-renowned software quality frameworks (ISO/IEC 25010, SOLID, Clean Code, cyclomatic complexity). ROI-of-refactoring estimates accompany every recommendation so engineering managers can justify the work to business stakeholders.

## Harness Flow Summary

| Step | Stage | Sub-skill Invoked |
|------|-------|-------------------|
| 0 | Code Intake & Scope Definition | — |
| 1 | Evaluation Framework Selection | `sub-evaluation-framework-selector` |
| 2 | Business Logic Tracing | `sub-business-logic-tracer` |
| 3 | Technical Quality Analysis | — (direct analysis) |
| 4 | Multi-Dimensional Scoring | `sub-scoring-engine` |
| 5 | Devil's Advocate Review (Quality Gate) | — |
| 6 | Improvement Roadmap Generation | `sub-improvement-roadmap` |
| 7 | Final Report Assembly | — |

## Sub-Skills

| File | Description |
|------|-------------|
| `skills/sub-evaluation-framework-selector.md` | Selects evaluation frameworks and tools based on language, framework, and audit scope |
| `skills/sub-business-logic-tracer.md` | Maps user-facing flows to code paths; identifies logic correctness and completeness issues |
| `skills/sub-scoring-engine.md` | Applies weighted ISO/IEC 25010 rubrics to produce dimensional scores (0–100) |
| `skills/sub-improvement-roadmap.md` | Generates prioritized, ROI-weighted improvement plan from validated audit findings |

## Tools Required

- `Read` — read source files from local repo or directory
- `Bash` — run static analysis tools (pylint, eslint, radon, sonar-scanner, etc.)
- `WebSearch` — fetch latest best practices, framework-specific guidelines, vulnerability disclosures
- `WebFetch` — crawl authoritative sources (ISO docs, refactoring.guru, OWASP, Martin Fowler)
- `Write` — produce the final audit report as a downloadable markdown document

## Knowledge Sources (for crawl pipeline)

- ArXiv: cs.SE (Software Engineering), cs.PL (Programming Languages)
- IEEE Transactions on Software Engineering
- ACM SIGSOFT / ICSE / FSE proceedings
- Refactoring.guru, MartinFowler.com, OWASP.org
- ISO/IEC 25010:2023 (SQuaRE — System and software quality models)
- SEI CERT Coding Standards

## Supporting Python Tools

- `tools/knowledge_updater.py` — crawls ArXiv cs.SE, IEEE Xplore abstracts, and authoritative SE blogs; appends scored entries to SECOND-KNOWLEDGE-BRAIN.md weekly

## Active Development Tasks

- [x] CLAUDE.md
- [x] PROJECT-detail.md
- [x] PROJECT-DEVELOPMENT-PHASE-TRACKING.md
- [x] SECOND-KNOWLEDGE-BRAIN.md
- [x] skills/main.md
- [x] skills/sub-evaluation-framework-selector.md
- [x] skills/sub-business-logic-tracer.md
- [x] skills/sub-scoring-engine.md
- [x] skills/sub-improvement-roadmap.md
- [x] tools/knowledge_updater.py
- [x] tools/schedule_cron.py
- [x] tools/run_knowledge_update.bat
- [x] tests/test-scenarios.md
- [x] tests/test_knowledge_updater.py
- [x] tests/execution-log-scenario1.md
- [x] tests/execution-log-scenario2.md
- [x] tests/execution-log-scenario3.md
- [x] tests/execution-log-scenario4.md
- [x] tests/execution-log-scenario5.md
- [x] tests/quality-gate-review.md
- [x] tests/cross-skill-compatibility-report.md
- [x] tests/fixtures/ (5 scenario codebases)
- [x] Cron schedule configured (Windows Task Scheduler)

## References

- [PROJECT-detail.md](PROJECT-detail.md) — Full technical specification
- [PROJECT-DEVELOPMENT-PHASE-TRACKING.md](PROJECT-DEVELOPMENT-PHASE-TRACKING.md) — Phase-by-phase build roadmap
- [SECOND-KNOWLEDGE-BRAIN.md](SECOND-KNOWLEDGE-BRAIN.md) — Self-improving domain knowledge base
