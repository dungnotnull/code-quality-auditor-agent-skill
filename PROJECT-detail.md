# PROJECT-detail.md — code-quality-auditor

## Executive Summary

The `code-quality-auditor` skill is a production-grade harness that transforms any source code repository into a structured, multi-dimensional professional audit report. It applies world-renowned software quality frameworks (ISO/IEC 25010:2023, SOLID principles, Clean Code metrics, OWASP Top 10, cyclomatic complexity) to produce scored findings, a business logic trace, and a ROI-weighted improvement roadmap.

The skill bridges the gap between raw static analysis output (which engineers can run themselves) and a strategic quality assessment that engineering managers and CTOs can use to justify technical debt remediation to business stakeholders.

---

## Problem Statement

**The core problem:** Most development teams know their codebase has quality issues, but cannot quantify, prioritize, or communicate them effectively.

- Static analysis tools produce hundreds of warnings without telling teams which ones actually matter
- Code reviews catch bugs but rarely surface systemic quality patterns
- Technical debt discussions with management fail because there is no business-impact framing
- Business logic correctness (as opposed to code style) is rarely audited systematically

**Domain context:** Software quality auditing is a mature practice in regulated industries (fintech, healthcare) but lacks accessible tooling for smaller teams. The WEF estimates that poor software quality costs the global economy over $1 trillion annually (CISQ/Consortium for IT Software Quality). Yet most codebases are never formally audited.

**Motivation:** This skill democratizes expert-level code quality auditing — making it accessible to any engineer or team through a structured, repeatable harness workflow.

---

## Target Users & Use Cases

### Primary Users
- **Tech leads / senior engineers** who need to communicate technical debt to management
- **CTOs** who have inherited a codebase and need a quality baseline before a major release
- **Developers** preparing for a security-sensitive deployment or compliance audit
- **Engineering managers** assigning quarterly refactoring priorities

### Trigger Examples

| User Says | Skill Does |
|---|---|
| "Audit my Python Flask app for code quality" | Full audit across all 6 dimensions → scored report |
| "I'm worried about the security of our payment module" | Targeted audit focused on Security + Reliability dimensions for payment-related files |
| "We're onboarding a new team — give me a codebase health report" | Full audit with emphasis on Maintainability and Complexity scores |
| "Our checkout API is slow — can you audit it?" | Targeted Performance + Complexity audit |
| "We have a compliance review next month — what's our risk exposure?" | Security + Reliability audit with regulatory framework mapping |
| "We want to prioritize technical debt work next quarter" | Full audit → improvement roadmap with effort/ROI estimates |

---

## Harness Architecture

```
User Input (code + context)
         │
         ▼
┌─────────────────────────────┐
│   Stage 0: Code Intake      │
│   - Source code retrieval   │
│   - Scope confirmation      │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Stage 1: Framework Selection       │
│  Sub-skill: sub-evaluation-         │
│  framework-selector                 │
│  Outputs: ISO/IEC 25010 chars,      │
│  tools, weights, supplementary      │
│  frameworks                         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Stage 2: Business Logic Tracing    │
│  Sub-skill: sub-business-logic-     │
│  tracer                             │
│  Outputs: flow map, [BL] findings   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Stage 3: Technical Quality         │
│  Analysis (direct)                  │
│  Read + Bash static analysis        │
│  Outputs: [TQ] findings (Dim 1–6)   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Stage 4: Scoring                   │
│  Sub-skill: sub-scoring-engine      │
│  Outputs: dimensional scores +      │
│  composite score + rationale        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Stage 5: Devil's Advocate Review   │
│  Quality Gate (in main harness)     │
│  - Challenge all findings           │
│  - Revise inflated/deflated scores  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Stage 6: Improvement Roadmap       │
│  Sub-skill: sub-improvement-roadmap │
│  Outputs: prioritized roadmap,      │
│  ROI estimates, quick wins          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Stage 7: Final Report Assembly     │
│  Write → markdown audit report      │
│  Quality gates check                │
│  Present to user                    │
└─────────────────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-evaluation-framework-selector

| Attribute | Detail |
|---|---|
| **File** | `skills/sub-evaluation-framework-selector.md` |
| **Purpose** | Selects ISO/IEC 25010 characteristics, static analysis tools, supplementary frameworks, and scoring weights |
| **Inputs** | Language, framework, domain, audit scope, known concerns |
| **Outputs** | Framework selection document with tool run commands and weight profile |
| **Tools Used** | WebSearch (look up language-specific best practice tools), WebFetch (retrieve ISO/OWASP docs) |
| **Quality Gate** | ≥4 characteristics selected; weights sum to 100%; ≥2 tools identified |

### sub-business-logic-tracer

| Attribute | Detail |
|---|---|
| **File** | `skills/sub-business-logic-tracer.md` |
| **Purpose** | Maps entry points to code paths; validates business rule correctness and completeness |
| **Inputs** | Source files (entry points, services, repositories), business purpose |
| **Outputs** | Flow map, [BL] findings with severity, file:line, business impact, recommended fix |
| **Tools Used** | Read (trace code path), Bash (grep for patterns, call graphs) |
| **Quality Gate** | ≥3 flows traced; all write operations checked for authorization and concurrency |

### sub-scoring-engine

| Attribute | Detail |
|---|---|
| **File** | `skills/sub-scoring-engine.md` |
| **Purpose** | Converts findings register to calibrated dimensional scores (0–100) + composite score |
| **Inputs** | Findings register, LOC count, domain context, scoring weights |
| **Outputs** | Score table, composite score, score rationale per characteristic |
| **Tools Used** | None (pure computation against findings) |
| **Quality Gate** | Each score has finding ID citations; calibration anchors verified; composite mathematically consistent |

### sub-improvement-roadmap

| Attribute | Detail |
|---|---|
| **File** | `skills/sub-improvement-roadmap.md` |
| **Purpose** | Prioritizes findings into ROI-weighted roadmap across 4 horizons: Quick Win / Short / Medium / Strategic |
| **Inputs** | Validated findings, scores, business context |
| **Outputs** | Four-horizon roadmap with effort, impact, ROI narrative, dependency map, composite score projection |
| **Tools Used** | None (pure synthesis from findings) |
| **Quality Gate** | ≥1 Quick Win; all items have ROI narrative; dependency chain identified |

---

## Skill File Format Specification

### Frontmatter Schema (all skill files)
```yaml
---
name: [kebab-case-name]
description: [One-line summary — used in /help and skill picker]
parent: [parent skill name, if sub-skill]  # omit for main skill
---
```

### Required Sections (main.md)
1. Role & Persona
2. Workflow (Harness Flow) — numbered stages and steps
3. Sub-skills Available
4. Tools (table format)
5. Output Format (exact template)
6. Quality Gates (checkbox list)

### Required Sections (sub-*.md)
1. Purpose (why this sub-skill exists)
2. Inputs (explicit parameter list)
3. Workflow (numbered steps)
4. Output (exact format template)
5. Quality Gate (checkbox list)

---

## E2E Execution Flow

```
1. User invokes /code-quality-auditor
2. Claude assumes Senior Software Quality Architect persona
3. Stage 0: Ask for code + context → confirm scope
4. Stage 1: Invoke sub-evaluation-framework-selector
   → If WebSearch unavailable: use SECOND-KNOWLEDGE-BRAIN.md frameworks list
5. Stage 2: Invoke sub-business-logic-tracer
   → Read entry points → trace 3–5 flows → record [BL] findings
6. Stage 3: Direct analysis
   → Run Bash static analysis tools (if available)
   → OR read files directly and analyze manually
   → Record [TQ] findings for 6 dimensions
7. Stage 4: Invoke sub-scoring-engine
   → Pass findings register → receive dimensional scores + composite
8. Stage 5: Devil's advocate review
   → Challenge each finding → revise if needed → document revisions
9. Stage 6: Invoke sub-improvement-roadmap
   → Pass validated findings + scores → receive 4-horizon roadmap with ROI
10. Stage 7: Assemble final report
    → Run quality gates checklist
    → Write report to file via Write tool (or stream inline)
    → Present to user
    → Offer follow-up: code-fix examples / section deep-dive / exec summary
```

**Error handling / graceful degradation:**
- If `Bash` is unavailable: perform manual static analysis by reading files; note in Appendix C
- If `WebSearch` is unavailable: use SECOND-KNOWLEDGE-BRAIN.md frameworks; note limitation
- If source code cannot be read (no path/URL): ask user to paste key files; reduce scope to pasted files
- If codebase is > 50,000 LOC: offer to scope to a specific module first

---

## SECOND-KNOWLEDGE-BRAIN Integration

The file `SECOND-KNOWLEDGE-BRAIN.md` is the living knowledge base for this skill. It stores:
- Core frameworks (ISO/IEC 25010, SOLID, Clean Code, etc.)
- Research papers on software quality
- Latest static analysis tool capabilities
- Authoritative data sources and URLs

The skill references SECOND-KNOWLEDGE-BRAIN.md when:
1. sub-evaluation-framework-selector needs to describe a framework
2. sub-business-logic-tracer needs domain-specific business logic patterns
3. WebSearch/WebFetch are unavailable (fallback mode)

`tools/knowledge_updater.py` updates SECOND-KNOWLEDGE-BRAIN.md on a weekly cron schedule by crawling ArXiv cs.SE, IEEE Xplore, and authoritative SE blogs.

---

## Quality Gates Definition

The following must all be true before presenting the final report:

1. **Evidence-grounded findings**: Every finding references a specific file:line (not generic advice)
2. **Named principle violations**: Every finding cites ISO/IEC 25010, SOLID, OWASP, or another named standard
3. **Score consistency**: Composite score matches the weighted sum of dimensional scores
4. **Business logic coverage**: At least 3 distinct user-facing flows were traced
5. **Devil's advocate review**: Stage 5 was completed; any revisions documented
6. **Quick win present**: At least one Quick Win item in the roadmap
7. **Security framing**: Security findings reference OWASP category or CVE where applicable
8. **Professional output**: Report reads as a professional document; not a chat reply

---

## Test Scenarios

See `tests/test-scenarios.md` for 5 concrete scenario-based test cases.

---


---

## Cluster B Integration

This skill (Skill 6: code-quality-auditor) shares three sub-skills with the other two skills in Cluster B:

| Sub-Skill | Shared With | Compatibility Status |
|---|---|---|
| sub-evaluation-framework-selector | Skill 4 (uiux-code-auditor), Skill 8 (website-auditor) | Compatible — added uiux and website domain profiles with corresponding tools |
| sub-scoring-engine | Skill 4, Skill 8 | Compatible — identical rubric, deduction schedule, and calibration anchors |
| sub-improvement-roadmap | Skill 4, Skill 8 | Compatible — same priority formula, time horizons, and ROI narrative format |

### Domain Profile Extensions

| Domain | Weight Profile | Unique Tools |
|---|---|---|
| UI/UX application | Usability 30%, Performance 20%, Maintainability 20%, Security 15%, Reliability 10%, Complexity 5% | axe-core, Lighthouse, stylelint, pa11y |
| Website | Performance 25%, Usability 25%, Security 20%, Compatibility 15%, Reliability 10%, Complexity 5% | Lighthouse, WAVE, SSL Labs, WebPageTest, HTTP Observatory |

### Sub-Skill Invocation Contract

All three Cluster B skills invoke the shared sub-skills with the same input/output contract:

`
# sub-evaluation-framework-selector
Input:  language, framework, domain, scope, known_concerns
Output: ISO 25010 chars, tools, supplementary frameworks, scoring weights
Gate:   ≥4 chars selected; weights sum to 100%; ≥2 tools identified

# sub-scoring-engine
Input:  findings_register, files_and_loc, domain_context, scoring_weights
Output: score per characteristic (0-100), composite score, rationale
Gate:   Every score has finding ID citations; calibration verified; composite consistent

# sub-improvement-roadmap
Input:  validated_findings, scores, business_context, score_weights
Output: 4-horizon roadmap with effort, impact, ROI narrative, dependencies
Gate:   ≥1 Quick Win; all items have ROI narrative; dependencies identified
`

### Cross-Reference Avoidance

SECOND-KNOWLEDGE-BRAIN.md Section 6.5 maps shared vs. unique knowledge entries across the cluster. When Skills 4 and 8 are built, they should reference shared entries from Skill 6 rather than duplicating them.

---

## Cluster B Integration

### Shared Sub-Skills

This skill (Skill 6: code-quality-auditor) shares three sub-skills with other Cluster B skills:

| Sub-Skill | Shared With | Interface Contract |
|---|---|---|
| sub-evaluation-framework-selector | Skill 4 (uiux-code-auditor), Skill 8 (website-auditor) | Same inputs (language, framework, domain, scope, known_concerns) and output format. Weight profiles and tool selections differ per domain. |
| sub-scoring-engine | Skill 4, Skill 8 | Same rubric, deduction schedule, calibration anchors, and composite formula. Only weight profiles differ (passed as input). |
| sub-improvement-roadmap | Skill 4, Skill 8 | Same priority formula, horizon thresholds, output format, and quality gates. Content differs per domain findings. |

### Sub-Skill Unique to Skill 6

| Sub-Skill | Description | Not Shared Because |
|---|---|---|
| sub-business-logic-tracer | Maps user-facing flows to code paths | UI/UX and website audits focus on visual/rendering correctness, not business rule correctness |

### Cross-Skill Compatibility

See 	ests/cross-skill-compatibility-report.md for the full compatibility validation. Key findings:
- All shared sub-skills use the same interface contract across Cluster B
- Same finding types produce the same score deductions regardless of invoking skill
- No duplicated knowledge base entries across Cluster B
- Each skill has unique domain knowledge (SOLID/Clean Code for Skill 6, WCAG/Nielsen for Skills 4/8)

### Cross-References in SECOND-KNOWLEDGE-BRAIN.md

Section 6.5 of SECOND-KNOWLEDGE-BRAIN.md documents which knowledge entries are shared across Cluster B and which are unique to each skill. This prevents duplication and enables cross-pollination.

## Key Design Decisions

1. **ISO/IEC 25010 as the organizing framework:** This international standard provides a stable, vendor-neutral taxonomy of software quality characteristics. It is recognized by ISO, IEC, IEEE, and most enterprise software procurement processes. Alternative (e.g., CISQ) was considered but ISO/IEC 25010 has broader industry recognition.

2. **Business logic tracing as a first-class audit stage:** Most code auditing tools focus purely on technical quality. Business logic correctness is equally important but nearly impossible to automate. Making it an explicit stage forces the auditor (Claude) to understand what the code is supposed to do before judging how it does it.

3. **Devil's advocate review (Stage 5) as a mandatory quality gate:** Without an explicit challenge phase, LLMs tend to over-flag issues (eager to find problems) or produce inconsistent severity ratings. The challenge phase improves calibration and reduces false positives.

4. **Four-horizon roadmap with ROI narratives:** Engineering recommendations without business framing are ignored. ROI narratives translate technical findings into business value — the language of decision-makers.

5. **Cluster B shared sub-skills:** sub-evaluation-framework-selector, sub-scoring-engine, and sub-improvement-roadmap are shared patterns across Cluster B (Skills 4, 6, 8). The sub-business-logic-tracer is unique to Skill 6.

6. **Cluster B shared sub-skills:** sub-evaluation-framework-selector, sub-scoring-engine, and sub-improvement-roadmap are shared patterns across Cluster B (Skills 4, 6, 8). The sub-business-logic-tracer is unique to Skill 6. Shared sub-skills use identical interface contracts but produce domain-specific outputs (different weight profiles, tool selections).

7. **Graceful degradation:** The skill must be usable even when Bash and WebSearch are unavailable (read-only, offline environments). The SECOND-KNOWLEDGE-BRAIN.md fallback ensures core functionality is always available.
