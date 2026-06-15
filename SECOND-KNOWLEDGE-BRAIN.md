# SECOND-KNOWLEDGE-BRAIN.md — code-quality-auditor

> **Self-improving knowledge base for the code-quality-auditor skill.**
> Updated weekly by `tools/knowledge_updater.py`. All human-added entries are marked `[Manual]`.
> Last updated: 2026-06-11

---

## 1. Core Concepts & Frameworks

### ISO/IEC 25010:2023 — Software and Systems Quality Requirements and Evaluation (SQuaRE)

The primary organizing framework for this skill. Defines eight top-level quality characteristics for software products:

| Characteristic | Key Sub-Characteristics | Relevance to Audit |
|---|---|---|
| **Functional Suitability** | Functional completeness, correctness, appropriateness | Maps to Business Logic Tracing (Stage 2) |
| **Performance Efficiency** | Time behaviour, resource utilisation, capacity | Stage 3 Dimension 4 (Performance) |
| **Compatibility** | Co-existence, interoperability | In-scope only for multi-system integrations |
| **Usability** | Appropriateness recognisability, learnability, operability | In-scope for UI code only |
| **Reliability** | Maturity, availability, fault tolerance, recoverability | Stage 3 Dimension 2 |
| **Security** | Confidentiality, integrity, non-repudiation, authenticity, accountability | Stage 3 Dimension 3 |
| **Maintainability** | Modularity, reusability, analysability, modifiability, testability | Stage 3 Dimensions 1 & 5 |
| **Portability** | Adaptability, installability, replaceability | In-scope for cloud-native / multi-env deployments |

**Key citation:** ISO/IEC 25010:2023, "Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model," International Organization for Standardization.

---

### SOLID Principles (Robert C. Martin)

Five object-oriented design principles central to the Maintainability dimension:

| Principle | Full Name | Violation Pattern |
|---|---|---|
| **S** | Single Responsibility Principle | Class/module does more than one thing; changes for multiple reasons |
| **O** | Open/Closed Principle | Adding a feature requires modifying existing code instead of extending it |
| **L** | Liskov Substitution Principle | Subclass breaks contracts of parent class; unexpected exceptions in subtypes |
| **I** | Interface Segregation Principle | Fat interfaces force implementing classes to depend on methods they don't use |
| **D** | Dependency Inversion Principle | High-level modules depend on concrete low-level modules; no abstraction layer |

**Source:** Martin, R.C. (2000). "Design Principles and Design Patterns." ObjectMentor.

---

### Clean Code Metrics (Robert C. Martin)

Quantitative thresholds derived from *Clean Code: A Handbook of Agile Software Craftsmanship*:

| Metric | Threshold | Action if Exceeded |
|---|---|---|
| Method length | > 20 lines: warning; > 30 lines: flag | Extract method |
| Class length | > 200 lines: warning; > 300 lines: flag | Extract class |
| Parameters per method | > 3: warning; > 5: flag | Introduce parameter object |
| Indentation depth | > 3 levels: flag | Extract guard clauses, early returns |
| Boolean flag parameters | Any: flag | Replace with two methods |
| Magic numbers | Any: flag | Extract named constant |

---

### Cyclomatic Complexity (McCabe, 1976)

A quantitative measure of the number of linearly independent paths through a function's source code.

**Formula:** CC = E − N + 2P (edges − nodes + 2 × connected components)

**Practical thresholds (SEI/McCabe guidelines):**

| CC Value | Risk Level | Recommended Action |
|---|---|---|
| 1–5 | Low | Well-structured; no action needed |
| 6–10 | Moderate | Consider simplifying |
| 11–20 | High | Should be refactored; harder to test |
| 21–50 | Very High | Must be refactored; high defect risk |
| > 50 | Critical | Untestable; immediate refactor required |

**Tool support:** Radon (Python), ESLint complexity rule (JS), PMD (Java), gocyclo (Go), NDepend (C#)

---

### Cognitive Complexity (SonarSource, 2018)

A measure of how difficult code is to understand — distinct from cyclomatic complexity in that it penalizes nesting and structural breaks more heavily.

**Key differences from cyclomatic complexity:**
- Nesting is penalized multiplicatively (deeper nesting = more penalty)
- Boolean sequences (&&, ||) add 1 each
- Structural elements that add no real complexity (catch, else) are not double-counted

**Reference:** Campbell, G.A. (2018). "Cognitive Complexity: A new way of measuring understandability." SonarSource White Paper.

---

### OWASP Top 10 (2021 Edition)

The standard reference for web application security risks. Relevant to Security dimension (Stage 3, Dimension 3):

| ID | Category | Common Code Patterns |
|---|---|---|
| A01 | Broken Access Control | Missing authorization checks; IDOR; path traversal |
| A02 | Cryptographic Failures | Hardcoded secrets; weak hashing (MD5/SHA1); unencrypted PII |
| A03 | Injection | Unsanitized SQL, command, LDAP, XPath queries; f-string SQL |
| A04 | Insecure Design | Missing threat modeling; no rate limiting; absent security controls by design |
| A05 | Security Misconfiguration | Debug mode in production; default credentials; verbose error messages |
| A06 | Vulnerable Components | Outdated dependencies with known CVEs |
| A07 | Auth/Identification Failures | Weak passwords; missing MFA; insecure session management |
| A08 | Software/Data Integrity Failures | Unverified CI/CD pipeline; unsigned package updates; insecure deserialization |
| A09 | Security Logging/Monitoring Failures | No logging of auth failures; logs not monitored; no alerting |
| A10 | Server-Side Request Forgery | User-controlled URLs passed to server-side HTTP requests without validation |

---

## 2. Key Research Papers

| Title | Authors | Year | Venue | DOI/Link | Relevance |
|---|---|---|---|---|---|
| "A Complexity Measure" | McCabe, T.J. | 1976 | IEEE TSE | 10.1109/TSE.1976.233837 | Foundation of cyclomatic complexity — the core metric for Complexity dimension |
| "An Empirical Study of the Impact of Technical Debt on Software Quality" | Zazworka et al. | 2011 | MTD | 10.1145/2000259.2000277 | Quantifies relationship between technical debt and defect rate |
| "The Impact of Code Smells on Software Change-Proneness: A Replication Study" | Zanoni et al. | 2016 | JSS | 10.1016/j.jss.2015.10.038 | Evidence base for code smell severity classification |
| "Cognitive Complexity: A new way of measuring understandability" | Campbell, G.A. | 2018 | SonarSource | sonarcloud.io/docs | Foundation for cognitive complexity metric |
| "Empirical Analysis of the ISO/IEC 25010 Quality Model" | Molléri et al. | 2020 | EASE | 10.1145/3383219.3383232 | Empirical validation of ISO 25010 characteristics in practice |
| "Do Code Smells Really Matter? A Mixed Methods Study" | Bavota et al. | 2015 | ICSE | 10.1109/ICSE.2015.197 | Empirical evidence linking specific smells to maintenance effort |
| "Technical Debt: From Metaphor to Theory and Practice" | Kruchten et al. | 2012 | IEEE Software | 10.1109/MS.2012.167 | Foundational technical debt theory used in roadmap ROI framing |
| "Measuring Software Coupling" | Briand et al. | 1999 | IEEE TSE | 10.1109/32.815326 | Formal definitions of coupling metrics used in Testability dimension |
| "OWASP Top 10:2021" | OWASP Foundation | 2021 | OWASP | owasp.org/Top10 | Security dimension framework |
| "Security Code Review: Best Practices" | SEI CERT | 2023 | SEI | sei.cmu.edu/CERT | Language-specific secure coding standards |

---

## 3. State-of-the-Art Methods & Tools

### Static Analysis Tools by Language

**Python:**
- `pylint` (v3.x) — comprehensive linter; detects 200+ issue types
- `radon` — cyclomatic complexity (`cc`), maintainability index (`mi`), Halstead metrics
- `bandit` — OWASP-aligned security linter for Python
- `mypy` — static type checking
- `vulture` — dead code detection
- `pyflakes` — lightweight undefined name / unused import checker

**JavaScript / TypeScript:**
- `eslint` (v9.x with flat config) — comprehensive linter
- `@typescript-eslint/parser` — TypeScript-specific rules
- `eslint-plugin-security` — OWASP-aligned security rules
- `jshint complexity` / `complexity-report` — Halstead + cyclomatic metrics
- `depcheck` — unused dependency detection

**Java:**
- `checkstyle` (v10.x) — style and coding standards
- `spotbugs` + `find-sec-bugs` — bug patterns + security
- `pmd` — duplication, complexity, best practices
- `sonarqube` (community edition) — comprehensive multi-dimensional analysis

**Go:**
- `golangci-lint` — aggregates 50+ linters (errcheck, staticcheck, gosec, dupl, gocyclo)
- `go vet` — built-in correctness checker

**Multi-language:**
- `semgrep` (v1.x) — polyglot pattern-based analysis; supports custom OWASP ruleset
- `sonarcloud` — cloud-based SonarQube for multi-language projects
- `snyk code` — SAST with AI-powered remediation suggestions

---

## 4. Authoritative Data Sources

| Source | URL | Type | Use Case |
|---|---|---|---|
| ISO/IEC 25010:2023 | iso.org/standard/35733.html | Standard | Quality model definition |
| OWASP Top 10 | owasp.org/www-project-top-ten | Standard | Security dimension |
| Refactoring.guru | refactoring.guru | Educational | Code smell catalog, refactoring patterns |
| Martin Fowler's Blog | martinfowler.com | Expert blog | Architecture, technical debt, DDD |
| SEI CERT Coding Standards | wiki.sei.cmu.edu/confluence/display/seccode | Standard | Language-specific secure coding |
| ArXiv cs.SE | arxiv.org/list/cs.SE/recent | Research | Latest software engineering papers |
| IEEE TSE | computer.org/csdl/journal/ts | Research | Peer-reviewed SE research |
| ACM SIGSOFT / ICSE | dl.acm.org | Research | Top conference proceedings |
| SonarSource Rules | rules.sonarsource.com | Tool docs | Rule-level quality issue descriptions |
| CISQ Standards | it-cisq.org/standards | Standard | Automated quality characteristic measurement |

---

## 5. Analytical Frameworks Used in This Skill

| Framework | Version | Scope | Reference |
|---|---|---|---|
| ISO/IEC 25010 | 2023 | Quality characteristic taxonomy + scoring organization | ISO |
| SOLID Principles | (Martin, 2000) | Maintainability dimension | ObjectMentor paper |
| Clean Code Metrics | (Martin, 2008) | Maintainability thresholds | Book: Clean Code |
| Cyclomatic Complexity | (McCabe, 1976) | Complexity dimension scoring | IEEE TSE 1976 |
| Cognitive Complexity | (Campbell, 2018) | Complexity dimension (cognitive burden) | SonarSource white paper |
| OWASP Top 10 | 2021 | Security dimension | OWASP Foundation |
| OWASP ASVS | 4.0 | Advanced security verification | OWASP Foundation |
| DRY Principle | (Hunt & Thomas, 1999) | Maintainability (duplication) | The Pragmatic Programmer |
| Law of Demeter | (Lieberherr & Holland, 1989) | Coupling measurement | OOPSLA 1989 |
| LCOM (Lack of Cohesion of Methods) | (Chidamber & Kemerer, 1994) | Cohesion measurement | IEEE TSE 1994 |

---

## 6. Self-Update Protocol

```python
# knowledge_updater.py — weekly crawl configuration

SOURCES = [
    {
        "type": "arxiv",
        "query": "software quality analysis code smell technical debt",
        "categories": ["cs.SE", "cs.PL"],
        "max_results": 20,
        "recency_days": 30
    },
    {
        "type": "web",
        "urls": [
            "https://martinfowler.com/bliki/TechnicalDebt.html",
            "https://refactoring.guru/refactoring/catalog",
            "https://owasp.org/www-project-top-ten/",
            "https://rules.sonarsource.com/",
            "https://wiki.sei.cmu.edu/confluence/display/seccode"
        ]
    },
    {
        "type": "arxiv",
        "query": "static analysis program analysis defect prediction",
        "categories": ["cs.SE"],
        "max_results": 10,
        "recency_days": 60
    }
]

SCORING = {
    "recency_weight": 0.4,    # Newer entries score higher
    "relevance_weight": 0.6,  # Keyword match score
    "keywords": [
        "code quality", "technical debt", "code smell", "refactoring",
        "cyclomatic complexity", "software metrics", "static analysis",
        "clean code", "SOLID", "ISO 25010", "maintainability",
        "security vulnerability", "OWASP", "defect prediction"
    ]
}

OUTPUT_FORMAT = """
### [{title}]({url})
**Authors:** {authors}
**Date:** {date}
**Source:** {venue}
**Relevance Score:** {score}/10
**Key Finding:** {abstract_summary}
**Added:** {crawl_date}
"""
```

---



#### Auto-crawled entries -- 2026-06-15

### [Wikipedia - Software Quality](https://en.wikipedia.org/wiki/Software_quality)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** Wikipedia - Software Quality  
**Relevance Score:** 5.7/10  
**Summary:** Refers to two related but distinct notions: functional quality and structural quality...
**Added:** 2026-06-15

### [[Code Smell](https://martinfowler.com/bliki/CodeSmell.html)](https://martinfowler.com/bliki/CodeSmell.html)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** Martin Fowler - Code Smell  
**Relevance Score:** 5.7/10  
**Summary:** A code smell is a surface indication that usually corresponds to a deeper problem in the system. The term was first coined by Kent Beck while helping me with my [Refactoring](https://martinfowler.com/books/refactoring.html) book....
**Added:** 2026-06-15

### [SonarQube Rules Guide](https://docs.sonarsource.com/sonarqube/latest/user-guide/rules/)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** SonarQube Rules Guide  
**Relevance Score:** 5.7/10  
**Summary:** For the complete documentation index, see [llms.txt](https://docs.sonarsource.com/llms.txt). This page is also available as [Markdown](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-rules/rules.md)....
**Added:** 2026-06-15

### [Wikipedia - Technical Debt](https://en.wikipedia.org/wiki/Technical_debt)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** Wikipedia - Technical Debt  
**Relevance Score:** 5.3/10  
**Summary:** Technical debtdesign debt[[]](https://en.wikipedia.org/wiki/Technical_debt#cite_note-Girish_2014-1) or code debt[system](https://en.wikipedia.org/wiki/System "System") that is attributable to choosing an expedient solution for its development.[[]](https://en.wikipedia.org/wiki/Technical_debt#cite_note-2) While an expedited solution can accelerate development in the short term, the resulting low qu...
**Added:** 2026-06-15

### [Catalog of Refactoring](https://refactoring.guru/refactoring/catalog)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** Refactoring Guru - Catalog  
**Relevance Score:** 4.8/10  
**Summary:** [ ](https://refactoring.guru/refactoring/catalog#checkout)[ ](https://refactoring.guru/refactoring/catalog#checkout)...
**Added:** 2026-06-15

### [[Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html)](https://martinfowler.com/bliki/TechnicalDebt.html)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** Martin Fowler - Technical Debt  
**Relevance Score:** 4.8/10  
**Summary:** Imagine I have a confusing module structure in my code base. I need to add a new feature. If the module structure was clear, then it would take me four days to add the feature but with this cruft, it takes me six days. The two day difference is the interest on the debt....
**Added:** 2026-06-15

### [OWASP Top Ten Web Application Security Risks](https://owasp.org/www-project-top-ten/)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** OWASP Top 10  
**Relevance Score:** 4.8/10  
**Summary:** The most current released version is the [OWASP Top Ten 2025](https://owasp.org/Top10/2025/)....
**Added:** 2026-06-15

### [JetBrains - Code Quality Analysis](https://www.jetbrains.com/help/pycharm/code-quality-analysis.html)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** JetBrains - Code Quality Analysis  
**Relevance Score:** 4.8/10  
**Summary:** [JetBrains](https://www.jetbrains.com/) [Products](https://www.jetbrains.com/products.html) [Pricing](https://www.jetbrains.com/store/) [Support](https://www.jetbrains.com/support/)...
**Added:** 2026-06-15

### [OWASP Application Security Verification Standard (ASVS) ](https://owasp.org/www-project-application-security-verification-standard/)
**Authors:** (Web resource)  
**Date:** 2026-06-15  
**Source:** Web  
**Category:** OWASP ASVS  
**Relevance Score:** 4.4/10  
**Summary:** ](https://creativecommons.org/licenses/by-sa/4.0/ "CC BY-SA 4.0") ](https://www.owasp.org/index.php/Category:OWASP_Project#tab=Project_Inventory) ](https://www.linkedin.com/company/owasp-asvs/)...
**Added:** 2026-06-15

### [GitHub Template Repositories: Served Domains, Maintenance, and Practitioner Guidelines](http://arxiv.org/abs/2606.14616v1)
**Authors:** Leuson Da Silva, Altaf Allah Abbassi, Imen Trabelsi et al.  
**Date:** 2026-06-12  
**Source:** ArXiv (cs.SE)  
**Category:** Software Metrics  
**Relevance Score:** 4.3/10  
**Summary:** Over time, GitHub has introduced different strategies for sharing reusable code artifacts. In addition to fork-based reuse, template repositories provide a distinct feature for generating new projects from scaffolding. Although this feature has been available since 2019, little is known about the domains it supports, its maintenance characteristics, or the practices that guide practitioners for ef...
**Added:** 2026-06-15


---

## 6.5. Cluster B Cross-Skill References

This section maps shared knowledge entries across Cluster B skills (Skills 4, 6, 8) to avoid duplication.

### Shared from Skill 6 (code-quality-auditor) — Reference by other Cluster B skills

| Knowledge Entry | Section | Used By |
|---|---|---|
| ISO/IEC 25010:2023 Quality Model | Section 1 | Skills 4, 6, 8 (shared framework) |
| SOLID Principles | Section 1 | Skills 4, 6 (code quality focus) |
| Clean Code Metrics | Section 1 | Skills 4, 6 (code quality focus) |
| Cyclomatic Complexity | Section 1 | Skills 4, 6, 8 (complexity dimension) |
| OWASP Top 10 (2021) | Section 1 | Skills 6, 8 (security dimension) |
| Scoring Rubric & Calibration | sub-scoring-engine.md | Skills 4, 6, 8 (shared scoring engine) |
| Roadmap Priority Formula | sub-improvement-roadmap.md | Skills 4, 6, 8 (shared roadmap) |
| Framework Selection Logic | sub-evaluation-framework-selector.md | Skills 4, 6, 8 (shared selector) |

### Unique to Skill 4 (uiux-code-auditor)

| Knowledge Entry | Notes |
|---|---|
| Nielsen's 10 Usability Heuristics | UI/UX-specific; not in Skill 6 KB |
| axe-core Accessibility Rules | UI testing tool; not in Skill 6 KB |
| React/Vue Component Anti-Patterns | Frontend-specific; not in Skill 6 KB |

### Unique to Skill 8 (website-auditor)

| Knowledge Entry | Notes |
|---|---|
| WCAG 2.2 Guidelines | Web accessibility standard; not in Skill 6 KB |
| Core Web Vitals (LCP, FID, CLS) | Web performance; not in Skill 6 KB |
| W3C Web Standards | Web compliance; not in Skill 6 KB |

---

---

## 6.5. Cluster B Cross-References

The following knowledge entries are also relevant to other Cluster B skills. This section prevents duplication and enables cross-pollination of domain knowledge.

### Entries Relevant to Skill 4 (uiux-code-auditor)

| Entry | Section | Why Relevant to Skill 4 |
|---|---|---|
| ISO/IEC 25010 — Usability characteristic | Section 1 | Primary focus of UI/UX audits |
| Nielsen's 10 Usability Heuristics | Section 5 | Core framework for UI quality evaluation |
| WCAG 2.1 (referenced in sub-evaluation-framework-selector) | Section 5 | Accessibility compliance framework |
| OWASP Top 10 — A03 (XSS) | Section 1 | Client-side security for UI code |

### Entries Relevant to Skill 8 (website-auditor)

| Entry | Section | Why Relevant to Skill 8 |
|---|---|---|
| ISO/IEC 25010 — All characteristics | Section 1 | Full website quality assessment |
| OWASP Top 10 (all 10 categories) | Section 1 | Website security evaluation |
| WCAG 2.1 | Section 5 | Website accessibility compliance |
| Static Analysis Tools — JavaScript/TypeScript | Section 3 | Frontend tooling for website audits |
| Performance Efficiency characteristic | Section 1 | Website performance evaluation |
| Lighthouse (referenced in tools) | Section 3 | Website performance + accessibility metrics |

### Entries Unique to Skill 6 (code-quality-auditor)

| Entry | Section | Not Needed By |
|---|---|---|
| SOLID Principles | Section 1 | Skills 4, 8 (UI-focused, not architecture-focused) |
| Clean Code Metrics | Section 1 | Skills 4, 8 (not code-style focused) |
| Cyclomatic Complexity | Section 1 | Skills 4, 8 (not complexity-focused) |
| Cognitive Complexity | Section 1 | Skills 4, 8 |
| DRY Principle, Law of Demeter, LCOM | Section 5 | Skills 4, 8 |

**Recommendation:** Skills 4 and 8 should reference this knowledge base for shared entries (OWASP, ISO 25010) rather than duplicating them. Skill-specific entries (SOLID, Clean Code, Complexity) should remain unique to Skill 6.

## 7. Knowledge Update Log

| Date | Source | Entries Added | Notes |
|---|---|---|---|
| 2026-06-11 | Manual (skill creation) | 10 core frameworks + 10 papers | Initial population during skill build |
| 2026-06-15 | knowledge_updater.py | 10 new entries | Automated weekly crawl |
