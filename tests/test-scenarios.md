# test-scenarios.md — code-quality-auditor

> Five scenario-based test cases for validating the `code-quality-auditor` skill harness.
> Each scenario defines: trigger input, expected workflow path, expected outputs, and pass/fail criteria.

---

## Scenario 1: Python Django E-Commerce Backend — Full Audit

**Context:** A startup's 3-year-old e-commerce platform has accumulated significant technical debt. The CTO wants a quality baseline before a Series A due diligence.

**Trigger Input:**
```
Audit this Django e-commerce backend for overall code quality.
Repo: https://github.com/example/shop-backend (hypothetical)
Language: Python 3.10 + Django 4.2 + DRF
Domain: E-commerce — product catalog, cart, checkout, orders
Scope: Full audit
Known pain points: Checkout sometimes throws 500 errors; adding new payment methods takes too long
```

**Expected Workflow Path:**
1. Stage 0: Scope confirmed — Python/Django, full audit, e-commerce domain
2. Stage 1: sub-evaluation-framework-selector selects: ISO 25010 all chars, Pylint + Radon + Bandit, OWASP Top 10, adjusted weights (Security 25% due to payment handling)
3. Stage 2: sub-business-logic-tracer traces: checkout flow, order placement, cart management (at minimum 3 flows); identifies duplicate-order risk and missing authorization on order history endpoint
4. Stage 3: Technical analysis finds SOLID violations in OrderService god class, N+1 queries in product listing, hardcoded Stripe test key in settings.py, bare except clauses in payment processor
5. Stage 4: sub-scoring-engine produces: Maintainability ~62, Security ~41 (hardcoded key), Performance ~58 (N+1), Reliability ~55 (bare excepts), Composite ~54 (Poor)
6. Stage 5: Devil's advocate review — confirms Critical findings are genuinely critical; may downgrade some Minor findings
7. Stage 6: sub-improvement-roadmap produces Quick Wins: remove hardcoded key, fix bare excepts; Short-term: fix N+1, add order idempotency; Strategic: decompose OrderService
8. Stage 7: Professional report assembled and presented

**Expected Outputs:**
- Composite score in range 45–65 (given described pain points)
- At least 2 Critical findings (hardcoded credentials + checkout reliability)
- Business logic finding for potential double-order race condition
- Quick Win for hardcoded Stripe key
- ROI narrative explaining that fixing checkout 500 errors directly protects revenue

**Pass Criteria:**
- [ ] All 7 stages executed in order
- [ ] Composite score is in the expected range with consistent dimensional scores
- [ ] hardcoded credentials finding classified as Critical Security issue
- [ ] N+1 query in product listing identified and classified as Major Performance issue
- [ ] Improvement roadmap has Quick Win for credential exposure
- [ ] Report passes all 8 quality gates
- [ ] Report reads as a professional audit document (headers, tables, file:line references)

---

## Scenario 2: React + TypeScript Frontend — Targeted Security & Performance Audit

**Context:** A B2B SaaS company wants to audit their admin dashboard frontend before a penetration test. They only care about security and performance — not code style.

**Trigger Input:**
```
Audit our React + TypeScript admin dashboard.
Language: TypeScript + React 18 + React Query + Zustand
Domain: B2B SaaS admin dashboard — user management, billing, analytics
Scope: Targeted — Security and Performance only
Known concerns: Dashboard feels slow; we're worried about XSS risks in the markdown renderer
```

**Expected Workflow Path:**
1. Stage 0: Scope confirmed — targeted audit, Security + Performance only
2. Stage 1: sub-evaluation-framework-selector scopes to only Security and Performance characteristics; selects ESLint + eslint-plugin-security + typescript-eslint; OWASP Top 10 (client-side focus: A03 XSS, A01 broken access control, A02 secrets in client code)
3. Stage 2: sub-business-logic-tracer focuses on user-facing flows that involve rendering user-controlled content (markdown renderer), data fetching patterns, and auth/authorization flows
4. Stage 3: Technical analysis limited to Security (Dim 3) and Performance (Dim 4): checks for unsafe innerHTML, unescaped markdown rendering, bundle size, unnecessary re-renders, React Query cache configuration
5. Stage 4: sub-scoring-engine produces scores ONLY for Security and Performance (not all 6 dimensions); notes partial audit
6. Stage 5: Devil's advocate: challenge whether any XSS risk is actually exploitable given the user population (internal admin users)
7. Stage 6: Roadmap focused on security + performance items only
8. Stage 7: Report clearly states "Targeted Audit: Security + Performance" in scope line

**Expected Outputs:**
- Only Security and Performance scores provided (not all 6 dimensions)
- XSS risk in markdown renderer identified (either confirmed or clearly ruled out with reasoning)
- Performance findings related to React rendering patterns
- Report scope section clearly documents the targeted nature of the audit

**Pass Criteria:**
- [ ] Skill correctly scopes to only the requested characteristics (does not audit Maintainability, Reliability, Testability, Complexity)
- [ ] XSS risk in markdown renderer is explicitly investigated and classified
- [ ] At least one React-specific performance finding (or an explicit "no performance issues found" statement with evidence)
- [ ] Report is clearly labeled as a Targeted Audit
- [ ] Devil's advocate review considers whether security findings are exploitable in context

---

## Scenario 3: Java Spring Boot Microservice — Security Focus (Fintech Domain)

**Context:** A fintech startup is preparing for a security audit by a third-party firm. They want to pre-audit their payment processing microservice.

**Trigger Input:**
```
Pre-audit our payment processing service before our external security review.
Language: Java 17 + Spring Boot 3.x + Spring Security + JPA/Hibernate
Domain: Fintech — payment processing, transaction records, refund management
Scope: Specific concern — Security + Reliability
Known concerns: We had one SQL injection attempt in our logs last quarter. We're worried about our transaction isolation levels.
```

**Expected Workflow Path:**
1. Stage 1: Framework selector applies fintech scoring weights (Security 30%, Reliability 25%); selects SpotBugs + FindSecBugs + OWASP ASVS level 2
2. Stage 2: Business logic tracer focuses on payment flow and refund flow; checks for transaction idempotency, concurrent transaction handling, authorization on financial operations
3. Stage 3: Security analysis uses OWASP Top 10 + CERT Java; Reliability analysis checks transaction boundaries, exception handling in payment path
4. Stage 4: Scoring uses fintech weights
5. Stage 5: Devil's advocate notes that SQL injection attempt in logs elevates urgency of any injection-related finding

**Expected Outputs:**
- Security findings reference OWASP categories explicitly
- Transaction isolation level analysis in Reliability dimension
- Any injection risk classified as Critical (given known attack attempts)
- ROI narrative references regulatory exposure (PCI-DSS, potential fines)

**Pass Criteria:**
- [ ] Fintech scoring weights applied (Security weight ≥ 25%)
- [ ] SQL injection risk explicitly investigated (whether present or absent)
- [ ] Transaction isolation and concurrent modification explicitly checked in business logic trace
- [ ] Any Critical security findings reference OWASP category (A03 Injection, etc.)
- [ ] ROI narratives mention regulatory/compliance context where relevant

---

## Scenario 4: Node.js REST API — Small Codebase (< 500 LOC)

**Context:** A freelance developer built a small Node.js API for a client. The client wants to understand the quality before taking ownership of the code.

**Trigger Input:**
```
Audit this Node.js API before I hand it over to my client.
Language: JavaScript (Node.js 20 + Express 4)
Domain: Internal HR tool — employee directory, leave requests
Scope: Full audit
Known concerns: None — just want an overall health check
```

**Expected Workflow Path:**
1. Stage 0: Small codebase (< 500 LOC) noted; full audit still performed but scope noted as limited
2. Stage 1: JS tooling selected (ESLint, npm audit); internal tooling domain → lower security weight
3. Stage 2: Business logic trace — may only find 2–3 entry points; traces all of them (not just 3)
4. Stage 3: For small codebase, density normalization is NOT applied (< 10,000 LOC)
5. Stage 4: Scores may be higher than expected (less code = fewer total issues); report is honest about small sample size
6. Stage 5: Devil's advocate — challenge whether findings in a 500-LOC codebase are representative or just outliers

**Expected Outputs:**
- Report acknowledges small codebase size and its implication for score reliability
- All entry points traced (not just 3 minimum)
- Scope limitation noted in Appendix C
- Scores may legitimately be 70–90 if the code is reasonably clean

**Pass Criteria:**
- [ ] Report states codebase size and notes any confidence limitations
- [ ] All (not just 3) entry points are traced since there are so few
- [ ] Scores above 70 are presented without inflating problems to fill a report
- [ ] Devil's advocate review challenges whether the small sample is representative
- [ ] Quick Wins section still present (even if only 1–2 items)

---

## Scenario 5: Legacy PHP Application — Critical State

**Context:** A company acquired a legacy PHP 5.6 e-commerce app. They need to understand how bad the situation is before deciding whether to rewrite or refactor.

**Trigger Input:**
```
Audit this legacy PHP application we just acquired.
Language: PHP 5.6 (no framework — procedural style)
Domain: E-commerce — product catalog, orders, customer accounts
Scope: Full audit
Known concerns: We suspect there are SQL injection vulnerabilities. The code was written in 2009 and has been patched by multiple contractors since. We need to know: rewrite or refactor?
```

**Expected Workflow Path:**
1. Stage 1: PHP-specific analysis (no modern framework — procedural); OWASP Top 10 critical; supplementary: SEI CERT C/PHP guidelines; all characteristics included; Security weight raised to 35% given stated SQL injection concern
2. Stage 2: Business logic trace — procedural code may not have clear entry points; identify include chains and form submission handlers as entry points
3. Stage 3: Security analysis will likely find: SQL injection (raw mysql_query with user input), no CSRF protection, md5 password hashing, session fixation risks. Complexity: deeply nested include files, spaghetti control flow.
4. Stage 4: Composite score likely in 15–35 range (Critical/Failing)
5. Stage 5: Devil's advocate — confirm that the low score is genuinely warranted by the evidence, not inflated by "legacy bias"
6. Stage 6: Roadmap includes Strategic item for "Evaluate full rewrite vs. incremental migration" with ROI analysis
7. Stage 7: Report explicitly addresses the rewrite-vs-refactor question in Executive Summary

**Expected Outputs:**
- Composite score in range 15–40 (Critical/Failing based on described state)
- SQL injection finding classified as Critical (A03)
- md5 password hashing classified as Critical (A02)
- Strategic roadmap item that addresses rewrite vs. refactor decision
- Executive Summary makes a clear recommendation on rewrite vs. refactor

**Pass Criteria:**
- [ ] SQL injection risk is identified and classified Critical
- [ ] Weak password hashing (md5/sha1) identified and classified Critical
- [ ] Composite score reflects genuinely poor state (< 45 expected)
- [ ] Devil's advocate confirms the low scores are evidence-backed (not "legacy bias")
- [ ] Strategic section of roadmap explicitly addresses rewrite vs. refactor with business ROI framing
- [ ] Executive Summary answers the user's actual question: rewrite or refactor?
- [ ] Report passes all 8 quality gates despite the low scores

---

## Test Execution Notes

When running these scenarios:

1. **Source code:** Use actual public repos or synthetic code samples that match the described scenario
2. **Expected score ranges:** These are approximate — a ±10 point variance is acceptable as long as scores are internally consistent
3. **Quality gate compliance:** The 8 quality gates in `skills/main.md` must all pass for a scenario to be considered passing
4. **Failure mode documentation:** If a scenario fails, document the specific gate that failed and the root cause in this file

### Common Failure Modes to Watch For

| Failure Mode | Symptom | Root Cause | Fix |
|---|---|---|---|
| Score inflation | All scores > 80 despite described problems | Devil's advocate review not enforced | Ensure Stage 5 is not skipped |
| Missing file:line | Findings say "somewhere in the service layer" | Stage 3 analysis was too shallow | Re-read specific files before flagging |
| No Quick Win | Roadmap has no Quick Win horizon | All findings treated as Strategic | Re-apply priority formula; simple security fixes are almost always Quick Wins |
| Business logic not traced | Report has no Flow Map | Stage 2 was skipped | Stage 2 is mandatory even for targeted audits |
| Generic advice | "You should add error handling" without specifics | Not enough code was read | Read the actual error-handling paths before flagging |
