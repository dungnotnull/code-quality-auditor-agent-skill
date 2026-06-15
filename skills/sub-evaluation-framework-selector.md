---
name: sub-evaluation-framework-selector
description: Selects the appropriate evaluation frameworks, quality characteristics, and static analysis tools for a code quality audit based on the language, framework, domain, and scope.
parent: code-quality-auditor
---

## Purpose

This sub-skill determines WHICH evaluation frameworks, quality models, and tooling to apply before the audit begins. Applying the wrong frameworks wastes effort and produces irrelevant findings. A Python data pipeline needs different quality dimensions than a React frontend or a Java microservice.

This sub-skill ensures every audit is grounded in named, citable methodologies — not ad hoc criteria.

---

## Inputs

- `language`: Primary programming language(s) (e.g., Python, JavaScript/TypeScript, Java, Go, C#)
- `framework`: Framework(s) in use (e.g., FastAPI, React, Spring Boot, Next.js, Django, Rails)
- `domain`: Application domain (e.g., fintech, healthcare, e-commerce, internal tooling, IoT)
- `scope`: Full audit / Targeted module / Specific concern (security, performance, etc.)
- `known_concerns`: Any pain points or incidents mentioned by the user

---

## Workflow

### Step 1: ISO/IEC 25010 Characteristic Selection

Review all eight top-level quality characteristics from ISO/IEC 25010:2023. Select which to include in this audit based on language, domain, and scope. Document the reasoning for any that are de-scoped.

| Characteristic | Include? | Condition |
|---|---|---|
| Functional Suitability | Always — maps to Business Logic Tracing stage | |
| Performance Efficiency | Always (include time behaviour, resource utilization) | |
| Compatibility | If multi-system integration present | |
| Usability | Only for UI-heavy code (React, Vue, frontend); skip for pure backend | |
| Reliability | Always | |
| Security | Always (amplify weight for fintech/healthcare/auth services) | |
| Maintainability | Always | |
| Portability | Only if multi-environment deployment is stated | |

For scoped audits: include only the requested characteristics plus always-on ones.

### Step 2: Language-Specific Static Analysis Tooling

Select tools based on the detected language(s). Prefer tools that produce parseable output (JSON/CSV) for score integration.

**Python:**
- Pylint — overall code quality, PEP 8, unused imports, naming
- Radon — cyclomatic complexity (cc), maintainability index (mi), raw metrics
- Bandit — security vulnerability scanning (OWASP-aligned)
- mypy — static type checking (if type hints are present)
- Coverage.py — test coverage report (if tests exist)

**JavaScript / TypeScript:**
- ESLint (with airbnb or recommended config) — style, complexity rules
- typescript-eslint — type safety analysis
- complexity-report — cyclomatic and Halstead metrics
- npm audit / Snyk — dependency vulnerability scan

**Java:**
- Checkstyle — coding standards (Google/Sun style)
- SpotBugs + FindSecBugs — bug patterns, security issues
- PMD — code duplication, complexity, best practices
- JaCoCo — test coverage

**Go:**
- golangci-lint (includes errcheck, staticcheck, gosec, dupl, gocyclo)
- go vet — correctness issues

**C# / .NET:**
- Roslyn Analyzers — built into dotnet SDK
- SonarAnalyzer.CSharp — security + quality
- NDepend (if available) — dependency metrics

**General (any language):**
- SonarQube / SonarCloud CLI (sonar-scanner) — if project has sonar config
- semgrep — polyglot static analysis with OWASP ruleset

**UI/UX-specific (for Skill 4 - uiux-code-auditor compatibility):**
- axe-core — automated accessibility testing (WCAG)
- Lighthouse — performance + accessibility + SEO audits
- stylelint — CSS/SCSS linting
- pa11y — accessibility testing CLI
- @storybook/react — component isolation for visual review

**Web-specific (for Skill 8 - website-auditor compatibility):**
- Lighthouse — Core Web Vitals (LCP, FID, CLS)
- WAVE — web accessibility evaluation
- SSL Labs (ssllabs.com) — TLS configuration audit
- WebPageTest — detailed performance profiling
- HTTP Observatory — security headers check

### Step 3: Supplementary Framework Selection

Select supplementary frameworks based on domain and language:

| Condition | Framework to Apply |
|---|---|
| Any web application | OWASP Top 10 (2021) for security dimension |
| Healthcare / HIPAA-adjacent | HIPAA technical safeguard checklist; NIST SP 800-53 controls |
| Financial / PCI-DSS adjacent | PCI-DSS requirement mapping (3.4, 6.3, 8.x) |
| UI/frontend code | Nielsen's 10 Usability Heuristics (minimal) |
| C / C++ / systems code | CERT C/C++ Coding Standard; MISRA C if embedded |
| API design | REST API design principles; OpenAPI schema validation |
| Async / concurrent code | Concurrency correctness checklist (race conditions, deadlocks, starvation) |
| **UI/UX code (Cluster B - Skill 4)** | Nielsen's 10 Usability Heuristics; WCAG 2.2 AA; Material Design / Human Interface Guidelines |
| **Website (Cluster B - Skill 8)** | WCAG 2.2; Core Web Vitals (LCP, FID, CLS); W3C Web Standards; CIS Benchmark for Web Apps |

### Step 4: Weighted Scoring Profile

Based on domain, adjust the default scoring weights for the composite score:

**Default weights (general application):**
- Maintainability: 20%
- Reliability: 20%
- Security: 20%
- Performance: 15%
- Testability: 15%
- Complexity: 10%

**Adjust for domain:**
- Fintech / Healthcare: Security weight → 30%, Performance → 20%, Maintainability → 15%, Reliability → 20%, Testability → 10%, Complexity → 5%
- Internal tooling / data pipeline: Performance → 25%, Maintainability → 25%, Security → 10%, Reliability → 20%, Testability → 15%, Complexity → 5%
- Public-facing API: Security → 25%, Reliability → 25%, Performance → 20%, Maintainability → 15%, Testability → 10%, Complexity → 5%
- **UI/UX application (Cluster B - Skill 4 compatibility):** Usability → 30%, Performance → 20%, Maintainability → 20%, Security → 15%, Reliability → 10%, Complexity → 5%
- **Website (Cluster B - Skill 8 compatibility):** Performance → 25%, Usability → 25%, Security → 20%, Compatibility → 15%, Reliability → 10%, Complexity → 5%

---

## Output

A structured framework selection document:

```
## Evaluation Framework Selection

**Language**: [...]
**Framework**: [...]
**Domain**: [...]
**Scope**: [...]

### ISO/IEC 25010 Characteristics Selected
| Characteristic | Included | Reason |
|---|---|---|
| Maintainability | Yes | Always included |
| Security | Yes | Always included; fintech domain increases weight |
| ... | | |

### Static Analysis Tools
| Tool | Language | What It Measures | Run Command |
|---|---|---|---|
| Pylint | Python | Code quality, PEP8 | `pylint src/ --output-format=json` |
| Radon cc | Python | Cyclomatic complexity | `radon cc src/ -s -j` |
| Bandit | Python | Security issues | `bandit -r src/ -f json` |
| ... | | | |

### Supplementary Frameworks
- OWASP Top 10 (2021): Applied to Security dimension
- [Other frameworks...]

### Scoring Weight Profile
| Characteristic | Weight |
|---|---|
| Maintainability | 20% |
| Security | 25% (adjusted for fintech) |
| ... | |
```

---



---

## Cluster B Compatibility Notes

This sub-skill is shared across Cluster B (Skills 4, 6, 8). The interface contract (inputs, outputs, quality gate) is identical for all three skills. The following adjustments are made per skill:

| Skill | Domain Focus | Key Weight Adjustments | Supplementary Frameworks |
|---|---|---|---|
| Skill 4 (uiux-code-auditor) | UI/UX code quality | Usability 30%, Accessibility 25%, Security 15% | WCAG 2.1, Nielsen Heuristics, axe-core |
| Skill 6 (code-quality-auditor) | Full code quality | Default weights; Security up to 35% for fintech/healthcare | OWASP, CERT, PCI-DSS |
| Skill 8 (website-auditor) | Full website audit | Security 25%, Accessibility 20%, Performance 20% | OWASP, WCAG 2.1, Lighthouse |

When this sub-skill is invoked from a different Cluster B skill, adjust:
1. The default weight profile to match the invoking skill's domain
2. The supplementary framework selection to include domain-specific frameworks (WCAG for Skills 4/8)
3. The tool selection to match the invoking skill's analysis focus (Lighthouse/axe for Skills 4/8)
## Quality Gate

Before returning to the parent skill:
- [ ] At least 4 ISO/IEC 25010 characteristics are included
- [ ] At least 2 static analysis tools are identified (or a reason given for why none can be run)
- [ ] Supplementary frameworks are selected for any domain-specific concerns
- [ ] Scoring weights sum to 100%
- [ ] All tool run commands are valid for the detected language/environment
