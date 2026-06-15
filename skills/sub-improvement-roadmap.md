---
name: sub-improvement-roadmap
description: Generates a prioritized, ROI-weighted improvement plan from validated audit findings, organized into four time horizons with effort estimates, impact scores, and risk levels.
parent: code-quality-auditor
---

## Purpose

A list of findings without a prioritization framework leaves engineering teams paralyzed — they don't know where to start. This sub-skill transforms the validated findings register into an actionable improvement roadmap that:

1. Separates quick wins (< 1 day, high ROI) from strategic architecture work
2. Estimates effort and business impact for each item
3. Provides an ROI narrative that engineering managers can use to justify the work
4. Identifies which improvements unblock other improvements (dependency order)

The output is a document an engineering team can paste into their sprint planning tool and start executing.

---

## Inputs

- `validated_findings`: Complete findings register (post-devil's-advocate review) with severity and file:line
- `scores`: Final dimensional scores per characteristic
- `business_context`: Domain, team size (if known), stated deadline constraints, known business priorities
- `score_weights`: Per-characteristic weights (from sub-evaluation-framework-selector)

---

## Prioritization Framework

### Priority Score Formula

For each finding group, calculate:

```
Priority Score = (Impact × 3) + (Urgency × 2) + (Ease × 1)
```

Where:
- **Impact (1–5):** How much does fixing this improve the composite score? 5 = Critical finding in high-weight characteristic; 1 = Minor finding in low-weight characteristic
- **Urgency (1–5):** How soon must this be addressed? 5 = Active production risk, exploitable security issue; 1 = Style improvement
- **Ease (1–5):** How easy is this to fix? 5 = One-line change or add null check; 1 = Full module rewrite

### Time Horizon Assignment

| Priority Score | Time Horizon |
|---|---|
| 18–30 | Quick Win (< 1 day, schedule immediately) |
| 12–17 | Short-Term (1–2 weeks, next sprint) |
| 7–11 | Medium-Term (1–3 months, upcoming quarter) |
| 1–6 | Strategic (3+ months, architectural planning) |

---

## Workflow

### Step 1: Group Related Findings

Findings that share a root cause or can be fixed in one refactoring effort should be grouped. Example: "14 instances of copy-pasted validation logic" is one improvement item, not 14.

Create improvement items from the findings. Each item may correspond to 1 or more finding IDs.

### Step 2: Score Each Item

Apply the priority formula. Be explicit about Impact, Urgency, and Ease scores with brief justification.

### Step 3: Assign to Time Horizon

Assign each item to a horizon based on its priority score.

### Step 4: Dependency Analysis

Identify items where one improvement enables or significantly accelerates another:

Example:
- "Extract UserService god class into focused services" (Strategic) ENABLES
- "Write unit tests for appointment logic" (Medium-Term) because tightly coupled code is untestable without the refactor

Mark dependencies with `→ Enables: [item name]`.

### Step 5: ROI Narrative

For each item, write a 1–2 sentence business ROI statement that a non-technical manager can understand.

Examples:
- "Fixing the null dereference in the payment path eliminates the most likely cause of checkout 500 errors, directly protecting revenue."
- "Removing copy-pasted validation logic (14 instances) means future requirement changes will require editing one place instead of 14 — reducing per-feature development time by an estimated 20%."
- "Adding missing authorization check on the admin API prevents unauthorized data access that could result in regulatory penalties under GDPR Article 83."

### Step 6: Quick Win Table

Summarize all Quick Win items in a compact table that a developer can use as a same-day action list.

---

## Output

A complete improvement roadmap:

```
## Improvement Roadmap

### Quick Wins (< 1 day effort — execute this sprint)

| # | Item | Finding IDs | Effort | Impact | Ease | Priority | ROI |
|---|---|---|---|---|---|---|---|
| QW-1 | Add null guard before profile access in PaymentService | TQ-012, BL-001 | 30 min | 5 | 5 | 30 | Eliminates top source of checkout 500 errors |
| QW-2 | Remove hardcoded API key in NotificationService, move to env var | TQ-023 | 1 hr | 4 | 5 | 27 | Closes exploitable security gap; prevents credential leakage |
| QW-3 | Replace bare `except: pass` in payment processing with specific exception handling | TQ-015 | 2 hrs | 4 | 4 | 22 | Restores error visibility in payment flow; ends silent failures |

**Quick Win Impact:** Addressing QW-1 through QW-3 is estimated to raise the Reliability score from 52 to ~72 and Security from 63 to ~78 — lifting the composite score from 66 to ~74 (+8 points) in under 4 hours of developer time.

---

### Short-Term Improvements (1–2 weeks — next sprint)

| # | Item | Finding IDs | Effort | Impact | Ease | Priority | ROI |
|---|---|---|---|---|---|---|---|
| ST-1 | Consolidate 14 copy-pasted validation routines into shared ValidationService | TQ-009 | 3 days | 4 | 3 | 17 | Future features require validating in 1 place, not 14; saves ~20% per-feature time |
| ST-2 | Refactor appointment scheduling to prevent double-booking (add DB constraint + service-layer lock) | BL-001 | 2 days | 5 | 3 | 17 | Eliminates double-booking risk; direct customer experience + revenue impact |
| ST-3 | Add dependency injection for NotificationService in AppointmentService | TQ-041 | 1 day | 3 | 4 | 15 | Makes AppointmentService unit-testable without triggering real notifications |

**Dependency:** ST-3 → Enables: Write unit tests for appointment booking flow

---

### Medium-Term Improvements (1–3 months — quarterly roadmap)

| # | Item | Finding IDs | Effort | Impact | Ease | Priority | ROI |
|---|---|---|---|---|---|---|---|
| MT-1 | Fix N+1 query in product listing endpoint (add eager loading / select_related) | TQ-031 | 3 days | 3 | 3 | 12 | Reduces product listing API response time from ~800ms to ~80ms under load |
| MT-2 | Reduce cyclomatic complexity of OrderProcessingService.process() from 24 to < 10 | TQ-051 | 5 days | 3 | 2 | 11 | Eliminates highest-complexity function; improves testability and reduces bug surface |
| MT-3 | Implement comprehensive unit test suite for appointment and payment flows | (multiple) | 10 days | 3 | 2 | 11 | Raises Testability score from 66 to ~82; enables safe refactoring of ST/MT items |

**Dependency:** MT-2 → Unblocked by: Strategic S-1 (dependency injection refactor makes testing viable)

---

### Strategic Improvements (3+ months — architectural planning)

| # | Item | Finding IDs | Effort | Impact | Ease | Priority | ROI |
|---|---|---|---|---|---|---|---|
| S-1 | Decompose UserService god class into UserProfileService, AuthService, UserPreferencesService | TQ-007 | 3 weeks | 4 | 1 | 6 | Long-term maintainability; enables team-level parallelism on user-related features |
| S-2 | Migrate data access layer to use repository pattern consistently (currently mixed direct ORM + raw SQL) | TQ-044, TQ-046 | 4 weeks | 3 | 1 | 5 | Reduces performance-related bugs; enables database abstraction for testing |

---

### Roadmap Summary

| Horizon | Items | Total Effort | Composite Score Improvement (est.) |
|---|---|---|---|
| Quick Wins | 3 | ~4 hours | +8 points (66 → 74) |
| Short-Term | 3 | ~6 days | +7 points (74 → 81) |
| Medium-Term | 3 | ~18 days | +5 points (81 → 86) |
| Strategic | 2 | ~7 weeks | +4 points (86 → 90) |
| **Full roadmap** | **11** | **~2.5 months** | **+24 points (66 → 90)** |
```

---



---

## Cluster B Compatibility Notes

This sub-skill is shared across Cluster B (Skills 4, 6, 8). The priority formula, time horizon thresholds, output format, and quality gates are identical for all three skills. The content of the roadmap items will differ based on each skill's domain findings, but the structure and prioritization logic is the same.

**Shared format guarantee:** Any Cluster B skill that invokes this sub-skill will produce a roadmap with the same 4-horizon structure, the same priority score formula, and the same ROI narrative requirement. This ensures that improvement plans from different Cluster B audits can be merged or compared by engineering teams.

## Quality Gate

Before returning to the parent skill:
- [ ] At least one Quick Win item is present (if none exist, re-examine findings — there is always a quick win)
- [ ] Every item has an explicit ROI narrative (business value statement, not just technical description)
- [ ] Effort estimates are realistic (do not underestimate strategic items; do not overestimate quick wins)
- [ ] Dependency relationships are identified and marked
- [ ] Roadmap summary table shows estimated composite score improvement per horizon
- [ ] All finding IDs referenced in the roadmap exist in the validated findings register
- [ ] Roadmap summary includes estimated composite score improvement per horizon and overall
