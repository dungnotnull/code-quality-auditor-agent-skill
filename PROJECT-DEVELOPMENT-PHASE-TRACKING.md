# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — code-quality-auditor

## Overview

This document tracks the phase-by-phase build roadmap for the `code-quality-auditor` skill. Each phase has a task list, deliverables, success criteria, and estimated effort.

**Current Status:** All phases (0–5) complete. Production-ready. All quality gates passing across 5 test scenarios.

---

## Phase 0: Research & Skill Architecture (Week 1–2)

**Goal:** Establish the theoretical foundation and skill architecture before writing any harness code.

### Tasks
- [x] Read ISO/IEC 25010:2023 quality model — identify all characteristics and sub-characteristics
- [x] Review SOLID principles and Clean Code metrics (Robert C. Martin)
- [x] Document cyclomatic complexity thresholds (McCabe, 1976; SEI guidelines)
- [x] Survey language-specific static analysis tooling (Python, JS, Java, Go)
- [x] Define harness stage sequence (Intake → Framework Selection → BL Tracing → Technical Analysis → Scoring → Roadmap → Report)
- [x] Design sub-skill boundaries (4 sub-skills identified)
- [x] Design scoring rubric (finding-based deduction with calibration anchors)
- [x] Write SECOND-KNOWLEDGE-BRAIN.md initial content

### Deliverables
- [x] `SECOND-KNOWLEDGE-BRAIN.md` — core frameworks, key papers, tool catalog
- [x] Harness architecture diagram (in PROJECT-detail.md)
- [x] Sub-skill boundaries defined

### Success Criteria
- All ISO/IEC 25010 quality characteristics mapped to audit dimensions
- Scoring rubric has calibration anchors with numeric ranges
- Sub-skill interfaces defined (inputs, outputs, quality gates)

### Estimated Effort: 8 hours

---

## Phase 1: Core Sub-Skills (Week 3–5)

**Goal:** Implement the 4 sub-skill files that are invoked by the main harness.

### Tasks
- [x] Write `sub-evaluation-framework-selector.md`
  - [x] ISO/IEC 25010 characteristic selection logic
  - [x] Language → tool mapping table (Python, JS, Java, Go, C#)
  - [x] Supplementary framework selection logic (OWASP, CERT, HIPAA)
  - [x] Scoring weight profiles by domain
- [x] Write `sub-business-logic-tracer.md`
  - [x] Entry point discovery procedure
  - [x] Business flow selection criteria
  - [x] Code path tracing template
  - [x] Business rule validation checklist
  - [x] Finding classification (Critical/Major/Minor)
- [x] Write `sub-scoring-engine.md`
  - [x] Finding-to-score deduction schedule
  - [x] Density normalization formula (LOC > 10,000)
  - [x] Calibration anchor table (score ranges → descriptions)
  - [x] Characteristic-to-finding-tag mapping
  - [x] Composite score formula
- [x] Write `sub-improvement-roadmap.md`
  - [x] Priority score formula (Impact × 3 + Urgency × 2 + Ease × 1)
  - [x] Time horizon assignment table
  - [x] Dependency analysis procedure
  - [x] ROI narrative template

### Deliverables
- [x] `skills/sub-evaluation-framework-selector.md`
- [x] `skills/sub-business-logic-tracer.md`
- [x] `skills/sub-scoring-engine.md`
- [x] `skills/sub-improvement-roadmap.md`

### Success Criteria
- Each sub-skill has explicit inputs, workflow, output format, and quality gate
- sub-scoring-engine produces consistent scores: same findings always produce the same score
- sub-improvement-roadmap always produces at least one Quick Win item
- All sub-skills can operate in graceful degradation mode (no WebSearch/Bash)

### Estimated Effort: 12 hours

---

## Phase 2: Main Harness + Quality Gates (Week 6–8)

**Goal:** Write the main harness skill file that orchestrates all sub-skills through the 7-stage workflow.

### Tasks
- [x] Write `skills/main.md` — full harness file
  - [x] Role & Persona section (Senior Software Quality Architect persona)
  - [x] Stage 0: Code Intake workflow (required inputs, confirmation protocol)
  - [x] Stage 1: Framework selection invocation
  - [x] Stage 2: Business logic tracing invocation
  - [x] Stage 3: Technical quality analysis (6 dimensions with detailed checklists)
  - [x] Stage 4: Scoring invocation
  - [x] Stage 5: Devil's advocate review (5-question challenge framework)
  - [x] Stage 6: Roadmap invocation
  - [x] Stage 7: Final report assembly
  - [x] Output Format (exact report template with all sections)
  - [x] Quality Gates checklist (8 gates)
- [x] Write `CLAUDE.md` — skill-level memory file
- [x] Write `PROJECT-detail.md` — full technical specification

### Deliverables
- [x] `skills/main.md`
- [x] `CLAUDE.md`
- [x] `PROJECT-detail.md`

### Success Criteria
- Harness file is complete enough for Claude to execute end-to-end without additional clarification
- Stage 5 devil's advocate review is not skippable
- Output format produces a professional-looking report, not a chat transcript
- All 8 quality gates are measurable (not vague)

### Estimated Effort: 8 hours

---

## Phase 3: SECOND-KNOWLEDGE-BRAIN Pipeline (Week 9–10)

**Goal:** Build the crawl4ai knowledge pipeline that keeps the skill self-improving.

### Tasks
- [x] Write `tools/knowledge_updater.py`
  - [x] ArXiv cs.SE crawler (using crawl4ai)
  - [x] IEEE Xplore abstract crawler
  - [x] Refactoring.guru sitemap crawler
  - [x] OWASP Top 10 changelog crawler
  - [x] Entry scoring (recency + relevance)
  - [x] Deduplication (DOI/URL hash check)
  - [x] Append to SECOND-KNOWLEDGE-BRAIN.md (structured format)
  - [x] Knowledge Update Log entry
- [x] Set up weekly cron schedule (see schedule skill)
- [x] Validate first crawl run produces valid entries

### Deliverables
- [x] `tools/knowledge_updater.py` — functional crawl4ai pipeline
- [x] First successful crawl run validated (unit tests pass, 36/36)
- [x] Cron schedule configured (tools/schedule_cron.py --dry-run verified)

### Success Criteria
- knowledge_updater.py runs without errors on a Python 3.11+ environment with crawl4ai installed
- Produces structured entries with: title, authors, date, DOI/URL, abstract, relevance score
- Deduplication correctly skips already-present entries
- First run adds at least 10 new entries to SECOND-KNOWLEDGE-BRAIN.md

### Estimated Effort: 6 hours

---

## Phase 4: Testing & Validation (Week 11–12)

**Goal:** Validate the skill against realistic test scenarios.

### Tasks
- [x] Write `tests/test-scenarios.md` (5 scenarios)
- [x] Execute Scenario 1: Python Django e-commerce (full audit)
- [x] Execute Scenario 2: React + TypeScript frontend (UI + performance focus)
- [x] Execute Scenario 3: Java Spring Boot microservice (security + reliability focus)
- [x] Execute Scenario 4: Node.js API (minimal codebase — < 500 LOC)
- [x] Execute Scenario 5: Legacy PHP application (critical state — expected low scores)
- [x] Review all outputs against quality gates
- [x] Identify gaps, edge cases, and failure modes
- [x] Update harness and sub-skills based on test findings

### Deliverables
- [x] `tests/test-scenarios.md`
- [x] Test execution log (markdown) for each scenario
- [x] Identified gaps and implemented fixes (see tests/execution_logs/gaps-and-fixes.md)

### Success Criteria
- All 5 scenarios produce valid reports that pass the 8 quality gates
- Quick Win items present in all scenario outputs
- Composite scores are internally consistent across scenarios
- Business logic trace covers ≥ 3 flows in all scenarios

### Estimated Effort: 10 hours

---

## Phase 5: Integration & Cross-Skill Wiring (Week 13–14)

**Goal:** Connect shared sub-skills across Cluster B (Skills 4, 6, 8) and validate consistency.

### Tasks
- [x] Verify sub-evaluation-framework-selector outputs are compatible with Skill 4 (uiux-code-auditor) and Skill 8 (website-auditor)
- [x] Verify sub-scoring-engine rubric is consistent across all three Cluster B skills
- [x] Verify sub-improvement-roadmap format is shared and consistent
- [x] Update PROJECT-detail.md references to reflect cluster integration
- [x] Cross-link SECOND-KNOWLEDGE-BRAIN.md entries from Skills 4 and 8 to avoid duplication

### Deliverables
- [x] Cross-skill compatibility validation report (tests/cross-skill-compatibility-report.md)
- [x] Updated sub-skill files with any cluster-level adjustments (uiux/website domain profiles added)
- [x] Updated SECOND-KNOWLEDGE-BRAIN.md with cross-references (Section 6.5)

### Success Criteria
- sub-evaluation-framework-selector can be invoked identically from Skills 4, 6, and 8
- sub-scoring-engine rubric produces consistent scores when same finding types appear in different skill audits
- No duplicated knowledge base entries across Cluster B skills

### Estimated Effort: 4 hours

---

## Total Estimated Effort Summary

| Phase | Weeks | Estimated Hours | Status |
|---|---|---|---|
| Phase 0: Research & Architecture | 1–2 | 8h | ✅ Complete |
| Phase 1: Core Sub-Skills | 3–5 | 12h | ✅ Complete |
| Phase 2: Main Harness + Quality Gates | 6–8 | 8h | ✅ Complete |
| Phase 3: Knowledge Pipeline | 9–10 | 6h | ✅ Complete |
| Phase 4: Testing & Validation | 11–12 | 10h | ✅ Complete |
| Phase 5: Cross-Skill Integration | 13–14 | 4h | ✅ Complete |
| **Total** | **14 weeks** | **48h** | **All phases complete** |
