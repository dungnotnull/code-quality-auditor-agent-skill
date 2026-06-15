---
name: sub-scoring-engine
description: Applies weighted ISO/IEC 25010 rubrics to the audit findings register and produces a normalized score (0–100) per quality characteristic plus a composite score, with full scoring rationale.
parent: code-quality-auditor
---

## Purpose

Translating a list of findings into a defensible, calibrated numeric score is the hardest part of a code audit. This sub-skill provides a systematic rubric-based scoring process that prevents both score inflation (being too generous) and score deflation (penalizing minor issues too heavily).

The goal is scores that a reasonable senior engineer would agree with after reading the findings list.

---

## Inputs

- `findings_register`: All `[BL]` and `[TQ]` tagged findings with severities (Critical / Major / Minor)
- `files_and_loc`: Number of files and approximate lines of code audited (for density normalization)
- `domain_context`: Application domain (affects security/reliability weight calibration)
- `scoring_weights`: Per-characteristic weights from sub-evaluation-framework-selector output

---

## Scoring Rubric

### Base Score Per Characteristic

Each characteristic starts at **100**. Points are deducted based on findings in that characteristic's scope.

**Deduction schedule:**

| Finding Severity | Points Deducted (per finding) |
|---|---|
| Critical | −15 to −25 (based on finding impact) |
| Major | −5 to −10 |
| Minor | −1 to −3 |

**Floor:** No characteristic score can go below 0.

**Density adjustment:** For codebases > 10,000 lines of code, normalize finding counts per 1,000 lines before applying deductions. This prevents large codebases from being unfairly penalized for having more total findings when their finding *density* is low. Do NOT apply density normalization for codebases under 10,000 LOC. For codebases under 500 LOC, add a confidence caveat in the score rationale (see main harness Stage 4).

**Normalization formula:**
```
Adjusted finding count = (raw finding count / total LOC) × 1000
Apply deductions based on adjusted counts (rounded to nearest integer)
```

### Characteristic-Specific Scoring Scope

Each ISO/IEC 25010 characteristic maps to specific finding tags:

| Characteristic | Finding Tags in Scope | What to Look For |
|---|---|---|
| Maintainability | [TQ] Dimension 1 findings + [BL] minor | SOLID violations, naming, duplication, dead code, method/class length |
| Reliability | [TQ] Dimension 2 findings + [BL] correctness | Unhandled exceptions, null dereference, race conditions, missing validations |
| Security | [TQ] Dimension 3 findings + [BL] authorization | OWASP Top 10 hits, hardcoded credentials, injection risks, insecure patterns |
| Performance | [TQ] Dimension 4 findings | N+1 queries, blocking I/O, O(n²) patterns, memory leaks |
| Testability | [TQ] Dimension 5 findings | Tight coupling, god objects, static state, absence of tests |
| Complexity | [TQ] Dimension 6 findings | Cyclomatic > 10, cognitive complexity, deep nesting, high coupling |

### Calibration Anchor Points

**Small codebase caveat:** For codebases under 500 LOC, high scores (80+) do NOT indicate production-readiness. Add explicit note: 'Scores reflect code quality for a small codebase. Production readiness requires additional capabilities (auth, persistence, tests) not assessed in code quality scoring.'

Use these anchor descriptions to cross-check scores:

| Score Range | Description |
|---|---|
| 90–100 | Excellent. Follows best practices consistently. Minor style issues only. |
| 75–89 | Good. Well-structured with a few moderate issues that don't affect core functionality. |
| 60–74 | Fair. Noticeable quality gaps; technical debt is accumulating. Needs attention within one quarter. |
| 40–59 | Poor. Multiple significant issues affecting reliability, maintainability, or security. Requires structured improvement effort. |
| 20–39 | Critical. Pervasive quality problems. High risk of production incidents. Major refactoring needed. |
| 0–19 | Failing. Fundamental quality failures across the board. Likely to cause systemic issues. |

---

## Workflow

### Step 1: Tally Findings Per Characteristic

Group all findings from the findings register by their ISO/IEC 25010 characteristic. Count Critical, Major, and Minor findings for each.

### Step 2: Apply Deductions

For each characteristic:
1. Apply density normalization if LOC > 10,000
2. Deduct points for each finding: assign impact points from the deduction schedule based on specific finding severity and nature
3. Calculate raw score = 100 − total deductions
4. Clamp to [0, 100]

### Step 3: Cross-Check with Calibration Anchors

Read the raw score and verify it matches the calibration anchor description for that range. If a score of 72 (Fair) is produced for Reliability but there are no Critical findings and only 2 Major findings, the score may be too low — recalibrate by reducing deduction amounts for those Major findings if they are of lower impact.

Document any calibration adjustments made.

### Step 4: Composite Score

```
Composite = Σ (characteristic_score × weight)
```

Round to the nearest integer.

### Step 5: Score Rationale

For each characteristic, write a 2–3 sentence rationale that:
- States the score and its anchor range
- Names the top 1–3 finding IDs that most contributed to any deductions
- Notes any mitigating positive observations

---

## Output

A complete scoring report:

```
## Multi-Dimensional Quality Scores

### Finding Summary (Input)
| Characteristic | Critical | Major | Minor | LOC Normalized? |
|---|---|---|---|---|
| Maintainability | 0 | 3 | 7 | No (4,200 LOC) |
| Reliability | 2 | 1 | 2 | No |
| Security | 1 | 2 | 1 | No |
| Performance | 0 | 2 | 3 | No |
| Testability | 0 | 3 | 2 | No |
| Complexity | 1 | 1 | 4 | No |

### Scores

| Characteristic | Raw Score | Calibration Check | Final Score |
|---|---|---|---|
| Maintainability | 78 | Matches "Good" — 3 Major (DRY violations, god class, naming) | **78/100** |
| Reliability | 52 | Matches "Poor" — 2 Critical (null deref BL-001, unhandled DB exception TQ-012) | **52/100** |
| Security | 63 | Matches "Fair" — 1 Critical (hardcoded API key TQ-023) | **63/100** |
| Performance | 74 | Matches "Fair/Good" — 2 Major (N+1 in product listing TQ-031, blocking I/O TQ-035) | **74/100** |
| Testability | 66 | Matches "Fair" — 3 Major coupling issues (TQ-041, 043, 047) | **66/100** |
| Complexity | 61 | Matches "Fair" — 1 Critical function (cyclomatic 24, TQ-051) + high LCOM | **61/100** |

### Composite Score
(78×0.20) + (52×0.20) + (63×0.20) + (74×0.15) + (66×0.15) + (61×0.10)
= 15.6 + 10.4 + 12.6 + 11.1 + 9.9 + 6.1 = **65.7 → 66/100** (Fair)

### Score Rationale

**Maintainability (78/100 — Good):** Three Major findings prevented an Excellent rating: a god class in UserService (TQ-007), 14 instances of copy-pasted validation logic (TQ-009), and inconsistent naming across the data layer (TQ-011). No Critical maintainability issues; the overall structure is reasonable.

**Reliability (52/100 — Poor):** Two Critical findings drive this score down significantly: a null dereference risk when the optional profile object is accessed without a guard (BL-001/TQ-012), and bare `except: pass` in the payment processing path (TQ-015). These represent real production incident risk.

[... etc. for all characteristics ...]
```

---



---

## Cluster B Compatibility Notes

This sub-skill is shared across Cluster B (Skills 4, 6, 8). The scoring rubric, deduction schedule, calibration anchors, and composite formula are identical for all three skills. The only difference is the weighting profile, which is passed as input from sub-evaluation-framework-selector (which adjusts weights per skill domain).

**Consistency guarantee:** If the same finding type (e.g., 'hardcoded API key, Critical') is submitted to this scoring engine from any Cluster B skill, it will receive the same deduction (-15 to -25) in the same characteristic (Security). The final score may differ only because the weight profile differs per skill domain.

## Quality Gate

Before returning to the parent skill:
- [ ] Every characteristic has a finding tally, a raw score, a calibration check, and a rationale
- [ ] Composite score is computed using the exact weights from sub-evaluation-framework-selector
- [ ] No score is assigned without at least one supporting finding ID (or a positive statement if score is high)
- [ ] Calibration anchors were checked — no score falls outside the descriptive range given the findings
- [ ] Density normalization was applied if total LOC > 10,000
